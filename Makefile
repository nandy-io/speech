.PHONY: install remove reset tag

install:
	kubectl create namespace speech-nandy-io

remove:
	kubectl delete namespace speech-nandy-io

reset: remove install

tag:
	-git tag -a "v$(VERSION)" -m "Version $(VERSION)"
	git push origin --tags
