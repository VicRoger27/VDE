#pragma once

#include <QObject>
#include <QQuickWindow>
#include "AppIndexer.h"
#include "FileSearcher.h"
#include "LocalAiClient.h"

class LauncherManager : public QObject {
    Q_OBJECT
    Q_PROPERTY(bool isVisible READ isVisible WRITE setVisible NOTIFY visibilityChanged)

public:
    explicit LauncherManager(QObject *parent = nullptr);
    ~LauncherManager() override = default;

    bool isVisible() const { return m_isVisible; }
    void setVisible(bool visible);

    void setWindow(QQuickWindow *window) { m_window = window; }
    QQuickWindow *window() const { return m_window; }

    AppIndexer *appIndexer() { return &m_appIndexer; }
    FileSearcher *fileSearcher() { return &m_fileSearcher; }
    LocalAiClient *aiClient() { return &m_aiClient; }

public slots:
    void toggle();
    void show();
    void hide();
    void query(const QString &text);

signals:
    void visibilityChanged(bool visible);
    void inferenceStateChanged(const QString &state, const QString &model);
    void externalQueryRequested(const QString &query);

private:
    bool m_isVisible = false;
    QQuickWindow *m_window = nullptr;
    AppIndexer m_appIndexer;
    FileSearcher m_fileSearcher;
    LocalAiClient m_aiClient;
};
