#include "LauncherManager.h"
#include <QDBusConnection>

LauncherManager::LauncherManager(QObject *parent)
    : QObject(parent)
{
    // Forward AI inference state changes
    connect(&m_aiClient, &LocalAiClient::inferenceStateChanged,
            this, &LauncherManager::inferenceStateChanged);

    // Register on D-Bus session bus
    QDBusConnection bus = QDBusConnection::sessionBus();
    if (bus.registerService("org.vde.Launcher")) {
        bus.registerObject("/Launcher", this, QDBusConnection::ExportAdaptors);
    }
}

void LauncherManager::setVisible(bool visible) {
    if (m_isVisible != visible) {
        m_isVisible = visible;
        if (m_window) {
            m_window->setVisible(m_isVisible);
            if (m_isVisible) {
                m_window->raise();
                m_window->requestActivate();
            }
        }
        emit visibilityChanged(m_isVisible);
    }
}

void LauncherManager::toggle() {
    setVisible(!m_isVisible);
}

void LauncherManager::show() {
    setVisible(true);
}

void LauncherManager::hide() {
    setVisible(false);
}

void LauncherManager::query(const QString &text) {
    show();
    emit externalQueryRequested(text);
}
