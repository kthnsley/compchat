import sys
import os
import subprocess

RootDir = (os.path.dirname(os.path.realpath(__file__)))
sys.path.append(RootDir + "/src")

Requirements = open("requirements")

# Verify requirements, fail if we do not have them
def verifyRequirements():
	RequirementsFailed = []
	for Requirement in Requirements.readlines():
		Requirement = Requirement.strip()
		try:
			__import__(Requirement)
		except:
			RequirementsFailed.append(Requirement)

	if len(RequirementsFailed) > 0:
		print(f"Missing requirements, can not install: [{', '.join(RequirementsFailed)}]")
		sys.exit(1)

def setup():
	import setuptools

	setuptools.setup(
		name="compchat",
		version="0.0.1",
		description=("COMP-3825 chat application project of Dylan Hensley and Brandon Wong."),
		packages=setuptools.find_packages("src"),
		package_dir={"": "src"},
		include_package_data=True,
	)
	

if __name__ == "__main__":
	verifyRequirements()
	if len(sys.argv) == 1:
		sys.argv += ["install", "--user"]
		
	setup()