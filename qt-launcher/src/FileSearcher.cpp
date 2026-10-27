#include "FileSearcher.h"
#include <QDir>
#include <QDirIterator>
#include <QFileInfo>
#include <QDesktopServices>
#include <QUrl>
#include <QtConcurrent/QtConcurrent>

FileSearcher::FileSearcher(QObject *parent)
    : QObject(parent)
{
    connect(&m_watcher, &QFutureWatcher<QVariantList>::finished, this, [this]() {
        m_isSearching = false;
        emit isSearchingChanged();
        emit searchCompleted(m_watcher.result());
    });
}

bool FileSearcher::isSearching() const {
    return m_isSearching;
}

void FileSearcher::searchFiles(const QString &query) {
    if (query.trimmed().isEmpty()) {
        emit searchCompleted(QVariantList());
        return;
    }

    if (m_watcher.isRunning()) {
        m_watcher.cancel();
    }

    m_isSearching = true;
    emit isSearchingChanged();

    QFuture<QVariantList> future = QtConcurrent::run([this, query]() {
        return doSearch(query);
    });
    m_watcher.setFuture(future);
}

QVariantList FileSearcher::doSearch(const QString &query) {
    QVariantList results;
    QString norm = query.trimmed().toLower();

    QStringList searchRoots;
    searchRoots << QDir::homePath() + "/Documents"
                << QDir::homePath() + "/Downloads"
                << QDir::homePath() + "/Pictures"
                << QDir::homePath() + "/Desktop";

    int count = 0;
    const int maxResults = 30;

    for (const QString &root : searchRoots) {
        if (!QDir(root).exists()) continue;

        QDirIterator it(root, QDir::Files | QDir::Readable, QDirIterator::Subdirectories);
        while (it.hasNext() && count < maxResults) {
            it.next();
            const QFileInfo info = it.fileInfo();
            const QString fileName = info.fileName();

            if (fileName.toLower().contains(norm)) {
                QVariantMap map;
                map["name"] = fileName;
                map["path"] = info.absoluteFilePath();
                map["size"] = info.size();
                map["suffix"] = info.suffix().toLower();
                map["lastModified"] = info.lastModified().toString("yyyy-MM-dd hh:mm");
                results.append(map);
                count++;
            }
        }
        if (count >= maxResults) break;
    }

    return results;
}

bool FileSearcher::openFile(const QString &filePath) {
    return QDesktopServices::openUrl(QUrl::fromLocalFile(filePath));
}
