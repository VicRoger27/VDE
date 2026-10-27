#include "AppIndexer.h"
#include <QDir>
#include <QFile>
#include <QTextStream>
#include <QProcess>
#include <QStandardPaths>
#include <algorithm>

AppIndexer::AppIndexer(QObject *parent)
    : QObject(parent)
{
    connect(&m_watcher, &QFileSystemWatcher::directoryChanged, this, &AppIndexer::onDirectoryChanged);
    scanDirectories();
}

int AppIndexer::totalApps() const {
    QMutexLocker locker(&m_mutex);
    return m_apps.size();
}

void AppIndexer::onDirectoryChanged(const QString &) {
    scanDirectories();
}

void AppIndexer::scanDirectories() {
    QMutexLocker locker(&m_mutex);
    m_apps.clear();

    QStringList appDirs;
    appDirs << "/usr/share/applications"
            << "/usr/local/share/applications"
            << QDir::homePath() + "/.local/share/applications";

    for (const QString &dirPath : appDirs) {
        QDir dir(dirPath);
        if (!dir.exists()) continue;

        if (!m_watcher.directories().contains(dirPath)) {
            m_watcher.addPath(dirPath);
        }

        const QStringList files = dir.entryList(QStringList() << "*.desktop", QDir::Files | QDir::Readable);
        for (const QString &file : files) {
            parseDesktopFile(dir.filePath(file));
        }
    }

    // Sort alphabetically by name
    std::sort(m_apps.begin(), m_apps.end(), [](const DesktopApp &a, const DesktopApp &b) {
        return a.name.toLower() < b.name.toLower();
    });

    locker.unlock();
    emit appsChanged();
}

void AppIndexer::parseDesktopFile(const QString &filePath) {
    QFile file(filePath);
    if (!file.open(QIODevice::ReadOnly | QIODevice::Text)) return;

    DesktopApp app;
    app.id = QFileInfo(filePath).fileName();

    QTextStream in(&file);
    bool inDesktopEntry = false;

    while (!in.atEnd()) {
        QString line = in.readLine().trimmed();
        if (line.isEmpty() || line.startsWith('#')) continue;

        if (line.startsWith('[')) {
            inDesktopEntry = (line == "[Desktop Entry]");
            continue;
        }

        if (!inDesktopEntry) continue;

        int eqIdx = line.indexOf('=');
        if (eqIdx == -1) continue;

        QString key = line.left(eqIdx).trimmed();
        QString val = line.mid(eqIdx + 1).trimmed();

        if (key == "Name" && app.name.isEmpty()) {
            app.name = val;
        } else if (key == "Exec" && app.exec.isEmpty()) {
            // Strip %f, %u, %F, %U arguments
            app.exec = val.replace(QRegularExpression("%[a-zA-Z]"), "").trimmed();
        } else if (key == "Icon" && app.icon.isEmpty()) {
            app.icon = val;
        } else if (key == "Comment" && app.comment.isEmpty()) {
            app.comment = val;
        } else if (key == "NoDisplay") {
            app.noDisplay = (val.toLower() == "true");
        } else if (key == "Keywords") {
            app.keywords = val.split(';', Qt::SkipEmptyParts);
        } else if (key == "Categories") {
            app.categories = val.split(';', Qt::SkipEmptyParts);
        }
    }

    if (!app.noDisplay && !app.name.isEmpty() && !app.exec.isEmpty()) {
        // Prevent duplicate IDs
        auto it = std::find_if(m_apps.begin(), m_apps.end(), [&](const DesktopApp &existing) {
            return existing.id == app.id || existing.name == app.name;
        });
        if (it == m_apps.end()) {
            m_apps.append(app);
        }
    }
}

QVariantList AppIndexer::getPinnedApps() {
    QMutexLocker locker(&m_mutex);
    QVariantList list;

    // Return the first 18 apps as default pinned items
    int limit = qMin(18, m_apps.size());
    for (int i = 0; i < limit; ++i) {
        const auto &app = m_apps[i];
        QVariantMap map;
        map["id"] = app.id;
        map["name"] = app.name;
        map["exec"] = app.exec;
        map["icon"] = app.icon;
        map["comment"] = app.comment;
        list.append(map);
    }
    return list;
}

QVariantList AppIndexer::getAllApps() {
    QMutexLocker locker(&m_mutex);
    QVariantList list;
    for (const auto &app : m_apps) {
        QVariantMap map;
        map["id"] = app.id;
        map["name"] = app.name;
        map["exec"] = app.exec;
        map["icon"] = app.icon;
        map["comment"] = app.comment;
        list.append(map);
    }
    return list;
}

int AppIndexer::calculateMatchScore(const DesktopApp &app, const QString &normalizedQuery) {
    const QString nameLower = app.name.toLower();
    if (nameLower == normalizedQuery) return 1000;
    if (nameLower.startsWith(normalizedQuery)) return 800 - (nameLower.length() - normalizedQuery.length());
    if (nameLower.contains(normalizedQuery)) return 500;

    for (const QString &kw : app.keywords) {
        if (kw.toLower().contains(normalizedQuery)) return 300;
    }

    if (app.exec.toLower().contains(normalizedQuery)) return 200;
    if (app.comment.toLower().contains(normalizedQuery)) return 100;

    return 0;
}

QVariantList AppIndexer::searchApps(const QString &query) {
    if (query.trimmed().isEmpty()) return getPinnedApps();

    QMutexLocker locker(&m_mutex);
    QString norm = query.trimmed().toLower();

    struct ScoredApp {
        DesktopApp app;
        int score;
    };

    QList<ScoredApp> scored;
    for (const auto &app : m_apps) {
        int score = calculateMatchScore(app, norm);
        if (score > 0) {
            scored.append({app, score});
        }
    }

    std::sort(scored.begin(), scored.end(), [](const ScoredApp &a, const ScoredApp &b) {
        return a.score > b.score;
    });

    QVariantList results;
    int limit = qMin(24, scored.size());
    for (int i = 0; i < limit; ++i) {
        QVariantMap map;
        map["id"] = scored[i].app.id;
        map["name"] = scored[i].app.name;
        map["exec"] = scored[i].app.exec;
        map["icon"] = scored[i].app.icon;
        map["comment"] = scored[i].app.comment;
        results.append(map);
    }
    return results;
}

bool AppIndexer::launch(const QString &execCommand) {
    if (execCommand.trimmed().isEmpty()) return false;
    return QProcess::startDetached(execCommand);
}
