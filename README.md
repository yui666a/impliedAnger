# 【notebookが使えるコンテナの設定】

1. 以下のコマンドで解凍する
> tar -zxvf docker_template_repressed-anger.tar.gz  

2. フォルダ名は各々変更後、cdコマンドでカレントディレクトリをそのフォルダ内にしてください  

3. `Makefile` 内の `PROJECT_NAME` となっている部分を各自ユニークな名前に変更

4. `docker-compose.yml` 内の `xxxx` となっている部分を各自ユニークな名前に変更(2箇所)  

5. 同じくその少し下の `ports` の `ZZZZ:ZZZZ` を変更  
（ホスト:コンテナ となっていますが、ホストは自由に決めてかまいません．  
コンテナ側は他のコンテナやサービスと競合してはいけないので、私たちは`7777`周辺を使うようにしましょう．  
これを書いているときは`7000`番台に何も動いていませんが、誰かと競合しないように `docker ps` コマンドを実行して PORTS の部分を確認し、すでに使われていないか確認してください．）

6. 同じくその少し下の `ports` の TensorBoard用の`VVVV:6006` を変更
コンテナ部のデフォルトは6006です．ホスト部は誰かと競合しないように自由に変更してください．

7. 以下のコマンドで`.docker`をコピーして、イメージ作成が始まります(そこそこ時間はかかります)
> cp -r .docker/ dir/.docker/  
> make up

8. 終わったあと、下のコマンドを実行してコンテナに入ってnotebookを起動 `ZZZZ`はコンテナのport
> (ksl-nn02) \$ docker exec -it <container_name> bash  
> (in cont.) $ jupyter notebook --ip=0.0.0.0 --port ZZZZ --allow-root

9. コマンドプロンプトで別タブを開き，下のコマンドのYYYY(ホスト) XXXX(コンテナ)に変更し、`localhost:YYYY` にブラウザでアクセスすればnotebookが見えるはずです
> ssh ksl-nn02 -L YYYY:ksl-nn02:XXXX -N`  

