#include "LauncherAdaptor.h"
#include "LauncherManager.h"

LauncherAdaptor::LauncherAdaptor(LauncherManager *parent)
    : QDBusAbstractAdaptor(parent)
    , m_manager(parent)
{
    setAutoRelaySignals(true);
}

void LauncherAdaptor::Toggle() {
    m_manager->toggle();
}

void LauncherAdaptor::Show() {
    m_manager->show();
}

void LauncherAdaptor::Hide() {
    m_manager->hide();
}

void LauncherAdaptor::Query(const QString &text) {
    m_manager->query(text);
}
