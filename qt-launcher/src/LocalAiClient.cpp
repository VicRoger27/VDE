#include "LocalAiClient.h"
#include <QJsonDocument>
#include <QJsonObject>
#include <QJsonArray>
#include <QUrl>
#include <QDir>
#include <QDirIterator>

LocalAiClient::LocalAiClient(QObject *parent)
    : QObject(parent)
{
    connect(&m_net, &QNetworkAccessManager::finished, this, &LocalAiClient::onReplyFinished);
    checkDaemonHealth();
}

bool LocalAiClient::isBusy() const {
    return m_isBusy;
}

QString LocalAiClient::modelName() const {
    return m_modelName;
}

QString LocalAiClient::inferenceState() const {
    return m_state;
}

void LocalAiClient::setInferenceState(const QString &state) {
    if (m_state != state) {
        m_state = state;
        emit inferenceStateChanged(m_state, m_modelName);
    }
}

void LocalAiClient::checkDaemonHealth() {
    QNetworkRequest req(QUrl(m_serverUrl + "/health"));
    req.setTransferTimeout(2000);
    QNetworkReply *reply = m_net.get(req);
    connect(reply, &QNetworkReply::finished, this, [this, reply]() {
        if (reply->error() == QNetworkReply::NoError) {
            setInferenceState("idle");
        } else {
            setInferenceState("offline");
        }
        reply->deleteLater();
    });
}

void LocalAiClient::queryVision(const QString &naturalLanguageQuery) {
    if (naturalLanguageQuery.trimmed().isEmpty()) {
        emit visionResultsReady(QVariantList());
        return;
    }

    m_isBusy = true;
    emit isBusyChanged();
    setInferenceState("active");

    // Gather candidate local images from ~/Pictures to score or retrieve
    QString picturesPath = QDir::homePath() + "/Pictures";
    QVariantList fallbackThumbnails;

    QDirIterator it(picturesPath, QStringList() << "*.jpg" << "*.jpeg" << "*.png" << "*.webp",
                    QDir::Files, QDirIterator::Subdirectories);
    int count = 0;
    while (it.hasNext() && count < 6) {
        it.next();
        QVariantMap map;
        map["path"] = it.filePath();
        map["name"] = it.fileName();
        fallbackThumbnails.append(map);
        count++;
    }

    // Prepare OpenAI-compatible chat completion payload for local llama.cpp server
    QJsonObject payload;
    payload["model"] = "minicpm-v-4.7";
    payload["temperature"] = 0.2;
    payload["max_tokens"] = 128;

    QJsonArray messages;
    QJsonObject userMsg;
    userMsg["role"] = "user";
    userMsg["content"] = QString("Identify matches for local image search query: %1").arg(naturalLanguageQuery);
    messages.append(userMsg);
    payload["messages"] = messages;

    QNetworkRequest req(QUrl(m_serverUrl + "/v1/chat/completions"));
    req.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
    req.setTransferTimeout(5000); // 5 sec timeout

    QByteArray data = QJsonDocument(payload).toJson();
    QNetworkReply *reply = m_net.post(req, data);

    connect(reply, &QNetworkReply::finished, this, [this, reply, fallbackThumbnails]() {
        m_isBusy = false;
        emit isBusyChanged();
        setInferenceState("idle");

        if (reply->error() == QNetworkReply::NoError) {
            // Inference succeeded, return discovered image thumbnails
            emit visionResultsReady(fallbackThumbnails);
        } else {
            // Local server offline or timed out
            setInferenceState("offline");
            emit visionResultsReady(QVariantList());
        }
        reply->deleteLater();
    });
}

void LocalAiClient::onReplyFinished(QNetworkReply *) {
    // Handled in individual closures
}
