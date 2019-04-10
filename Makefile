.PHONY: subscriptions install update reset remove

subscribe:
	kubectl create configmap -n speech-nandy-io subscriptions --from-file subscriptions/redis.yaml --dry-run -o yaml | kubectl create -f -

unsubscribe:
	kubectl delete configmap -n speech-nandy-io subscriptions

install:
	kubectl create -f kubernetes/namespace.yaml

update:
	kubectl replace -f kubernetes/namespace.yaml

remove:
	kubectl delete -f kubernetes/namespace.yaml

reset: remove install
