docker_build('api-speech-nandy-io', './api')
docker_build('daemon-speech-nandy-io', './daemon')
docker_build('gui-speech-nandy-io', './gui')

k8s_yaml(kustomize('.'))

k8s_resource('api', port_forwards=['18380:80', '18348:5678'])
k8s_resource('daemon', port_forwards=['28348:5678'])
k8s_resource('gui', port_forwards=['8380:80'])
