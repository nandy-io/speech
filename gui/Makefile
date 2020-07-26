ACCOUNT=nandyio
IMAGE=speech-gui
VERSION=0.3
NAME=$(IMAGE)-$(ACCOUNT)
NETWORK=klot.io
VOLUMES=-v ${PWD}/www/:/opt/service/www/ \
		-v ${PWD}/etc/docker.conf:/etc/nginx/conf.d/default.conf
PORT=8371

.PHONY: cross build network shell run start stop push install update remove reset

cross:
	docker run --rm --privileged multiarch/qemu-user-static:register --reset

build:
	docker build . --build-arg BASE=$(BASE) -t $(ACCOUNT)/$(IMAGE):$(VERSION)

network:
	-docker network create $(NETWORK)

shell: network
	-docker run -it --rm --name=$(NAME) --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh

run: network
	docker run --rm --name=$(NAME) --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) -p 127.0.0.1:$(PORT):80 --expose=80 $(ACCOUNT)/$(IMAGE):$(VERSION)

start: network
	docker run -d --name=$(NAME) --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) -p 127.0.0.1:$(PORT):80 --expose=80 $(ACCOUNT)/$(IMAGE):$(VERSION)

stop:
	docker rm -f $(NAME)

push:
	docker push $(ACCOUNT)/$(IMAGE):$(VERSION)

install:
	kubectl create -f kubernetes/gui.yaml

update:
	kubectl replace -f kubernetes/gui.yaml

remove:
	-kubectl delete -f kubernetes/gui.yaml

reset: remove install
