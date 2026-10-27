#pragma once

#include <QDBusAbstractAdaptor>
#include <QString>

class LauncherManager;

class LauncherAdaptor : public QDBusAbstractAdaptor {
    Q_OBJECT
    Q_CLASSINFO("D-Bus Interface", "org.vde.Launcher")

public:
    explicit LauncherAdaptor(LauncherManager *parent);
    ~LauncherAdaptor() override = default;

public slots:
    void Toggle();
    void Show();
    void Hide();
    void Query(const QString &text);

signals:
    void VisibilityChanged(bool visible);
    void InferenceStateChanged(const QString &state, const QString &model);

private:
    LauncherManager *m_manager;
};
