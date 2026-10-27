#pragma once

#include <QObject>
#include <QString>
#include <QVariantList>
#include <QVariantMap>
#include <QNetworkAccessManager>
#include <QNetworkReply>

class LocalAiClient : public QObject {
    Q_OBJECT
    Q_PROPERTY(bool isBusy READ isBusy NOTIFY isBusyChanged)
    Q_PROPERTY(QString modelName READ modelName CONSTANT)
    Q_PROPERTY(QString inferenceState READ inferenceState NOTIFY inferenceStateChanged)

public:
    explicit LocalAiClient(QObject *parent = nullptr);
    ~LocalAiClient() override = default;

    bool isBusy() const;
    QString modelName() const;
    QString inferenceState() const;

    Q_INVOKABLE void queryVision(const QString &naturalLanguageQuery);
    Q_INVOKABLE void checkDaemonHealth();

signals:
    void isBusyChanged();
    void inferenceStateChanged(const QString &state, const QString &model);
    void visionResultsReady(const QVariantList &results);

private slots:
    void onReplyFinished(QNetworkReply *reply);

private:
    void setInferenceState(const QString &state);

    QNetworkAccessManager m_net;
    QString m_serverUrl = "http://127.0.0.1:8080";
    QString m_modelName = "MiniCPM-V 4.7 1B";
    QString m_state = "idle";
    bool m_isBusy = false;
};
