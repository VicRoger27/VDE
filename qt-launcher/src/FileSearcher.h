#pragma once

#include <QObject>
#include <QString>
#include <QVariantList>
#include <QVariantMap>
#include <QFutureWatcher>

class FileSearcher : public QObject {
    Q_OBJECT
    Q_PROPERTY(bool isSearching READ isSearching NOTIFY isSearchingChanged)

public:
    explicit FileSearcher(QObject *parent = nullptr);
    ~FileSearcher() override = default;

    bool isSearching() const;

    Q_INVOKABLE void searchFiles(const QString &query);
    Q_INVOKABLE bool openFile(const QString &filePath);

signals:
    void isSearchingChanged();
    void searchCompleted(const QVariantList &results);

private:
    QVariantList doSearch(const QString &query);

    bool m_isSearching = false;
    QFutureWatcher<QVariantList> m_watcher;
};
