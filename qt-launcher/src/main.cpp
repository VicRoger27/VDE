#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <QQmlContext>
#include <QDir>
#include <QQuickWindow>
#include <QCommandLineParser>
#include "LauncherManager.h"

int main(int argc, char *argv[]) {
    // Enable High DPI scaling
    QGuiApplication::setHighDpiScaleFactorRoundingPolicy(
        Qt::HighDpiScaleFactorRoundingPolicy::PassThrough);

    QGuiApplication app(argc, argv);
    app.setApplicationName("vde-launcher");
    app.setOrganizationName("VDE");

    QCommandLineParser parser;
    parser.setApplicationDescription("VDE Start Menu Runner & Fast Local Indexer");
    parser.addHelpOption();
    QCommandLineOption daemonOption(QStringList() << "d" << "daemon", "Start in background daemon mode");
    parser.addOption(daemonOption);
    parser.process(app);

    bool isDaemon = parser.isSet(daemonOption);

    // Resolve assets path
    QString appDir = QCoreApplication::applicationDirPath();
    QString assetsDir = appDir + "/../assets";
    if (!QDir(assetsDir).exists()) {
        assetsDir = "/usr/local/share/vde/assets";
    }
    if (!QDir(assetsDir).exists()) {
        assetsDir = appDir + "/assets";
    }

    LauncherManager manager;

    QQmlApplicationEngine engine;
    engine.rootContext()->setContextProperty("launcherManager", &manager);
    engine.rootContext()->setContextProperty("appIndexer", manager.appIndexer());
    engine.rootContext()->setContextProperty("fileSearcher", manager.fileSearcher());
    engine.rootContext()->setContextProperty("aiClient", manager.aiClient());
    engine.rootContext()->setContextProperty("assetsDir", QUrl::fromLocalFile(assetsDir).toString());

    const QUrl url(QStringLiteral("qrc:/Vde/qml/Main.qml"));
    QObject::connect(&engine, &QQmlApplicationEngine::objectCreated,
                     &app, [url, &manager, isDaemon](QObject *obj, const QUrl &objUrl) {
        if (!obj && url == objUrl)
            QCoreApplication::exit(-1);

        auto *window = qobject_cast<QQuickWindow*>(obj);
        if (window) {
            manager.setWindow(window);
            if (isDaemon) {
                window->hide();
            } else {
                manager.show();
            }
        }
    }, Qt::QueuedConnection);

    engine.load(url);

    return app.exec();
}
