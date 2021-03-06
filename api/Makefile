ACCOUNT=nandyio
IMAGE=speech-api
VERSION=0.3
NAME=$(IMAGE)-$(ACCOUNT)
NETWORK=klot.io
VOLUMES=-v ${PWD}/lib/:/opt/service/lib/ \
		-v ${PWD}/test/:/opt/service/test/ \
		-v ${PWD}/bin/:/opt/service/bin/ \
		-v ${PWD}/config/:/opt/service/config/
ENVIRONMENT=-e REDIS_HOST=redis-klotio \
			-e REDIS_PORT=6379 \
			-e REDIS_CHANNEL=nandy.io/speech
PORT=8365

.PHONY: cross build network shell test run start stop push install update remove reset

cross:
	docker run --rm --privileged multiarch/qemu-user-static:register --reset

build:
	docker build . -t $(ACCOUNT)/$(IMAGE):$(VERSION)

network:
	-docker network create $(NETWORK)

shell: network
	-docker run -it --rm --name=$(NAME) --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) $(ACCOUNT)/$(IMAGE):$(VERSION) sh

test:
	docker run -it $(VOLUMES) $(ACCOUNT)/$(IMAGE):$(VERSION) sh -c "coverage run -m unittest discover -v test && coverage report -m --include lib/*.py"

run: network
	docker run --rm --name=$(NAME) --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) -p 127.0.0.1:$(PORT):80 --expose=80 $(ACCOUNT)/$(IMAGE):$(VERSION)

start: network
	docker run -d --name=$(NAME) --network=$(NETWORK) $(VOLUMES) $(ENVIRONMENT) -p 127.0.0.1:$(PORT):80 --expose=80 $(ACCOUNT)/$(IMAGE):$(VERSION)

stop:
	docker rm -f $(NAME)

push:
	docker push $(ACCOUNT)/$(IMAGE):$(VERSION)

install:
	kubectl create -f kubernetes/api.yaml

update:
	kubectl replace -f kubernetes/api.yaml

remove:
	-kubectl delete -f kubernetes/api.yaml

reset: remove install
