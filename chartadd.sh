cd helm-chart-sources
helm pull elastic/elasticsearch

cd ..
helm repo index --url https://sushilsanjaybhile.github.io/helmcharts/ --merge index.yaml .
git add .
git commit -m "merged index.html"
git push
