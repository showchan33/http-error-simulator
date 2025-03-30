# http-error-simulatorについて

HTTPの500系のステータスコードを意図的に発生させるツールです。<br>
Flaskで起動しているWebサーバーの前段にNginxをリバースプロキシとして設置し、各パスにリクエストした際にどのようなレスポンスが返るかを確認します。

# 使い方

## Docker Compose を使う場合

### セットアップ

```
cd docker
docker compose up -d
```

### 動作確認

nginxのコンテナに入ります。

```
docker exec -it nginx bash
```

curlを実行して、どのようなレスポンスが返るかを確認します。
```
(コンテナ内で実行)
curl http://localhost
curl http://localhost/slow
curl http://localhost/abort
curl http://localhost/nothing
```

## Tilt を使う場合

### セットアップ

```
tilt up
```

以下のようなKubernetesのリソースが作成されることを確認します。<br><br>
※ Ingress NGINX Controllerが``nginx``というIngressClass名でインストールされていることを前提とします。

```
$ kubectl get pod,svc,deploy,ing -l app.kubernetes.io/managed-by=tilt
NAME                                     READY   STATUS    RESTARTS   AGE
pod/http-error-simulator-8c8bc6c-n6jps   1/1     Running   0          24m

NAME                           TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)   AGE
service/http-error-simulator   ClusterIP   10.43.111.242   <none>        80/TCP    5d

NAME                                   READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/http-error-simulator   1/1     1            1           5d

NAME                                               CLASS   HOSTS   ADDRESS      PORTS   AGE
ingress.networking.k8s.io/http-error-sim-ingress   nginx   *       172.23.0.2   80      25h
```

### 動作確認

curlを実行するPodを立ち上げて、コンテナに入ります。

```
kubectl run curl --image=alpine/curl --command -- tail -f /dev/null
kubectl exec -it curl -- sh
```

どのようなレスポンスが返るかを確認します。

```
(コンテナ内で実行)
curl http://[ingress-nginxのドメイン名]
curl http://[ingress-nginxのドメイン名]/slow
curl http://[ingress-nginxのドメイン名]/abort
curl http://[ingress-nginxのドメイン名]/nothing
```

#### ``[ingress-nginxのドメイン名]``の確認方法

以下のコマンドで、 Ingress NGINX Controllerのサービス名を確認します。

```
kubectl get svc -A -l app.kubernetes.io/instance=ingress-nginx
```

例えば次のような出力だったとします。

```
NAMESPACE   NAME                                 TYPE           CLUSTER-IP     EXTERNAL-IP   PORT(S)                      AGE
default     ingress-nginx-controller             LoadBalancer   10.43.74.100   172.23.0.2    80:31836/TCP,443:31225/TCP   217d
```

この場合、``[ingress-nginxのドメイン名]`` は ``ingress-nginx-controller.default.svc.cluster.local``です。
