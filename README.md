# 【notebookが使えるコンテナの設定】

1. 以下のコマンドで解凍する
> tar -zxvf docker_template-implied_anger.tar.gz  

2. フォルダ名は各々変更後、cdコマンドでカレントディレクトリをそのフォルダ内にしてください  

3. `Makefile` 内の `PROJECT_NAME` となっている部分を各自ユニークな名前に変更

4. .envファイルの定数を指示にそって設定する

5. 以下のコマンドで`.docker`をコピーして、イメージ作成が始まります(そこそこ時間はかかります)
> cp -r .docker/ dir/.docker/  
> make build && make up

6. 終わったあと、下のコマンドを実行してコンテナに入ってnotebookを起動
> (ksl-nn02) docker exec -it {container_name} bash  
> (in container) jupyter lab --ip=0.0.0.0 --port 8888 --allow-root  
> (in container) tensorboard --logdir /home/nb-user/{path/to/log} --port 6006 --host 0.0.0.0  

もしくは

> sudo docker exec -t {container_name} jupyter lab --ip=0.0.0.0 --port 8888 --allow-root  
> sudo docker exec -t {container_name} tensorboard --logdir /home/nb-user/{path/to/log} --port 6006 --host 0.0.0.0  

7. 自分のPCで Terminal/コマンドプロンプト を開き，下のコマンドの `XXXX` や `YYYY` を .env で設定した `JUPYTER_LAB_PORT` と `TENSORBOARD_PORT` に変更し、自分のPCのブラウザから `localhost:XXXX`  や `localhost:YYYY` にアクセスすれば notebook や TensorBoard が見えるはずです

> `ssh ksl-nn02 -L XXXX:ksl-nn02:XXXX -L YYYY:ksl-nn02:YYYY -N`  
> 例） `ssh ksl-nn02 -N -L 7790:ksl-nn02:7790 -L 7791:ksl-nn02:7791 -N`  

