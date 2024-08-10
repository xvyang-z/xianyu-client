```
git checkout master
cd src
pyside6-deploy.exe -c .\pysidedeploy.spec
Robocopy.exe ./.assets ../out/main.dist/.assets /e
cp ../go/TG.exe ../out/TG.exe
git checkout dev
```

- 首次分发 ./out/main.dist 和 ./out/TG.exe即可
- 运行中产生的数据将保存在 main.dist 同级的 data 目录下