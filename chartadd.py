import os, yaml
import shutil

chartDir = "helm-chart-sources"
chartUntarDir = "helm-chart-untar-sources"

os.system("mkdir " + chartDir + " 2> /dev/null")
os.system("mkdir " + chartUntarDir + " 2> /dev/null")
chartLogoDict = {}
repoDict = {"elastic": "https://helm.elastic.co", "gitlab": "https://charts.gitlab.io/", "bitnami": "https://charts.bitnami.com/bitnami"}

chartList = ["gitlab/gitlab", "gitlab/fluentd-elasticsearch", "gitlab/gitlab-runner", "gitlab/elastic-stack", "bitnami/cert-manager", "bitnami/prometheus", "bitnami/postgresql", "bitnami/postgresql-ha", "bitnami/kibana", "elastic/elasticsearch", "oci://ghcr.io/nginxinc/charts/nginx-ingress"]


def pullUntarCmd(chart):
	os.system("helm pull --untar " + chart)

def pullTarCmd(chart):
	os.system("helm pull " + chart)

def helmRepoAddFunc(repo, repoURL):
	os.system("helm repo add " + repo + " " + repoURL)

def updateRepoFunc():
	os.system("helm repo update")

def createLogoDict():
	for subdir, dirs, files in os.walk("./helm-chart-untar-sources"):
		for file in files:
			if "Chart.yaml" == file:
				fp = open(subdir + "/" + file)
				yml = yaml.safe_load(fp)
				try:
					iconURL = yml["icon"]
					chartName = yml["name"]
				except:
					continue
				chartLogoDict[chartName] = iconURL

	f = open('url.txt', 'w')
	f.write( repr(chartLogoDict) + '\n' )
	f.close()

def deleteUntarDir(mydir):
	try:
		shutil.rmtree(mydir)
	except OSError as e:
		print("Error: %s - %s." % (e.filename, e.strerror))

# Add repos
for repo in repoDict:
	helmRepoAddFunc(repo, repoDict[repo])

# Update repos
updateRepoFunc()

# pull chart and untar them
os.chdir("helm-chart-sources")
for chart in chartList:
	pullTarCmd(chart)

os.chdir("../helm-chart-untar-sources")
for chart in chartList:
	pullUntarCmd(chart)

os.chdir("../")
createLogoDict()
deleteUntarDir("helm-chart-untar-sources")
#exit
#cd ..
#helm repo index --url https://sushilsanjaybhile.github.io/helmcharts/ --merge index.yaml .
#git add .
#git commit -m "merged index.html"
#git push
