docker_build('gui-speech-nandy-io', './gui')
docker_build('api-speech-nandy-io', './api')
docker_build('daemon-speech-nandy-io', './daemon')

k8s_yaml(kustomize('.'))

k8s_resource('gui', port_forwards=['6583:80'])
k8s_resource('api', port_forwards=['16583:80', '16551:5678'])
k8s_resource('daemon', port_forwards=['26551:5678'])
