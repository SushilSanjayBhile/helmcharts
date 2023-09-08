import os, yaml, json
import shutil

chartDir = "helm-chart-sources"
chartUntarDir = "helm-chart-untar-sources"

os.system("mkdir " + chartDir + " 2> /dev/null")
os.system("mkdir " + chartUntarDir + " 2> /dev/null")
chartLogoDict = {}
repoDict = {"elastic": "https://helm.elastic.co", "gitlab": "https://charts.gitlab.io/", "bitnami": "https://charts.bitnami.com/bitnami"}

chartList = ["gitlab/gitlab", "gitlab/fluentd-elasticsearch", "gitlab/gitlab-runner", "gitlab/elastic-stack", "bitnami/cert-manager", "bitnami/prometheus", "bitnami/postgresql", "bitnami/postgresql-ha", "bitnami/kibana", "elastic/elasticsearch", "oci://ghcr.io/nginxinc/charts/nginx-ingress"]


def pullUntarCmd(chart):
	cmd = "helm pull --untar " + chart
	print("Executing: " + cmd)
	os.system(cmd)

def pullTarCmd(chart):
	cmd = "helm pull " + chart
	print("Executing: " + cmd)
	os.system(cmd)

def helmRepoAddFunc(repo, repoURL):
	cmd = "helm repo add " + repo + " " + repoURL
	print("Executing: " + cmd)
	os.system(cmd)

def updateRepoFunc():
	os.system("helm repo update")

def createLogoDict():
	chartLogoDict = {}
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
	#chartLogoDict = chartLogoDict.replace("'", "\"")
	print(json.dumps(chartLogoDict))
	f.write( repr(chartLogoDict) + '\n' )
	f.close()

def deleteUntarDir(mydir):
	try:
		shutil.rmtree(mydir)
	except OSError as e:
		print("Error: %s - %s." % (e.filename, e.strerror))

# Add repos
print("\nAdding Repos...\n")
for repo in repoDict:
	helmRepoAddFunc(repo, repoDict[repo])

# Update repos
print("\nUpdating Repos...\n")
updateRepoFunc()

# pull chart and untar them
print("\nPulling chart tar file...\n")
os.chdir("helm-chart-sources")
for chart in chartList:
	pullTarCmd(chart)

print("\nPulling chart untar file...\n")
os.chdir("../helm-chart-untar-sources")
for chart in chartList:
	pullUntarCmd(chart)

os.chdir("../")
createLogoDict()
deleteUntarDir("helm-chart-untar-sources")

os.system("helm repo index . --url=https://sushilsanjaybhile.github.io/helmcharts/")
os.system("hit status; git add .; git status; git commit -m \"merged index.html\"; git push")
