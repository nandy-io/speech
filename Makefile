VERSION?=0.4
TILT_PORT=28380
.PHONY: up down tag untag

up:
	mkdir -p config
	echo "speakers:\n- docker-desktop" > config/settings.yaml
	echo "- op: add\n  path: /spec/template/spec/volumes/0/hostPath/path\n  value: $(PWD)/config" > tilt/config.yaml
	kubectx docker-desktop
	-kubectl label node docker-desktop speech.nandy.io/speakers=enabled
	tilt --port $(TILT_PORT) up

down:
	kubectx docker-desktop
	tilt down

tag:
	-git tag -a "v$(VERSION)" -m "Version $(VERSION)"
	git push origin --tags

untag:
	-git tag -d "v$(VERSION)"
	git push origin ":refs/tags/v$(VERSION)"
