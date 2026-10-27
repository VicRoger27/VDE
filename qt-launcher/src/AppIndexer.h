#pragma once

#include <QObject>
#include <QString>
#include <QVariantList>
#include <QVariantMap>
#include <QFileSystemWatcher>
#include <QMutex>

struct DesktopApp {
    QString id;
    QString name;
    QString exec;
    QString icon;
    QString comment;
    QStringList keywords;
    QStringList categories;
    bool noDisplay = false;
};

class AppIndexer : public QObject {
    Q_OBJECT
    Q_PROPERTY(int totalApps READ totalApps NOTIFY appsChanged)

public:
    explicit AppIndexer(QObject *parent = nullptr);
    ~AppIndexer() override = default;

    int totalApps() const;

    Q_INVOKABLE QVariantList getPinnedApps();
    Q_INVOKABLE QVariantList getAllApps();
    Q_INVOKABLE QVariantList searchApps(const QString &query);
    Q_INVOKABLE bool launch(const QString &execCommand);

signals:
    void appsChanged();

private slots:
    void onDirectoryChanged(const QString &path);

private:
    void scanDirectories();
    void parseDesktopFile(const QString &filePath);
    int calculateMatchScore(const DesktopApp &app, const QString &normalizedQuery);

    QList<DesktopApp> m_apps;
    QFileSystemWatcher m_watcher;
    mutable QMutex m_mutex;
};
