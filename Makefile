build_ui:
	cd ui && ng build --output-path=dist --prod
	cp ./ui/Dockerfile ./ui/dist
	-rsync -avuzbh ui/dist/ picam-controller:ui/
	ssh pi@picam-controller 'docker build -t ui ./ui'

restart_ui:
	ssh pi@picam-controller 'sudo systemctl restart ui'

deploy_ui: build_ui restart_ui

upload_controller:
	rsync -avuzbh --exclude '.venv' controller/ picam-controller:api/

upload_camera1:
	-rsync -avuzbh --exclude '.venv' camera/ picam-cam1:api/
upload_camera2:
	-rsync -avuzbh --exclude '.venv' camera/ picam-cam2:api/
upload_camera3:
	-rsync -avuzbh --exclude '.venv' camera/ picam-cam3:api/
upload_camera4:
	-rsync -avuzbh --exclude '.venv' camera/ picam-cam4:api/
upload_camera5:
	-rsync -avuzbh --exclude '.venv' camera/ picam-cam5:api/
upload_camera6:
	-rsync -avuzbh --exclude '.venv' camera/ picam-cam6:api/

restart_controller:
	ssh pi@picam-controller 'sudo systemctl restart controller'

stop_camera1:
	-ssh picam-cam1 'sudo systemctl stop camera'
stop_camera2:
	-ssh picam-cam2 'sudo systemctl stop camera'
stop_camera3:
	-ssh picam-cam3 'sudo systemctl stop camera'
stop_camera4:
	-ssh picam-cam4 'sudo systemctl stop camera'
stop_camera5:
	-ssh picam-cam5 'sudo systemctl stop camera'
stop_camera6:
	-ssh picam-cam6 'sudo systemctl stop camera'

start_camera1:
	-ssh picam-cam1 'sudo systemctl start camera'
start_camera2:
	-ssh picam-cam2 'sudo systemctl start camera'
start_camera3:
	-ssh picam-cam3 'sudo systemctl start camera'
start_camera4:
	-ssh picam-cam4 'sudo systemctl start camera'
start_camera5:
	-ssh picam-cam5 'sudo systemctl start camera'
start_camera6:
	-ssh picam-cam6 'sudo systemctl start camera'

restart_camera1:
	-ssh picam-cam1 'sudo systemctl restart camera'
restart_camera2:
	-ssh picam-cam2 'sudo systemctl restart camera'
restart_camera3:
	-ssh picam-cam3 'sudo systemctl restart camera'
restart_camera4:
	-ssh picam-cam4 'sudo systemctl restart camera'
restart_camera5:
	-ssh picam-cam5 'sudo systemctl restart camera'
restart_camera6:
	-ssh picam-cam6 'sudo systemctl restart camera'

update_camera1:
	-ssh picam-cam1 'cd api && pyenv activate camera && pipenv install && pipenv update'
update_camera2:
	-ssh picam-cam2 'cd api && pyenv activate camera && pipenv install && pipenv update'
update_camera3:
	-ssh picam-cam3 'cd api && pyenv activate camera && pipenv install && pipenv update'
update_camera4:
	-ssh picam-cam4 'cd api && pyenv activate camera && pipenv install && pipenv update'
update_camera5:
	-ssh picam-cam5 'cd api && pyenv activate camera && pipenv install && pipenv update'
update_camera6:
	-ssh picam-cam6 'cd api && pyenv activate camera && pipenv install && pipenv update'

upload_cameras: upload_camera1 upload_camera2 upload_camera3 upload_camera4 upload_camera5 upload_camera6
stop_cameras: stop_camera1 stop_camera2 stop_camera3 stop_camera4 stop_camera5 stop_camera6
start_cameras: start_camera1 start_camera2 start_camera3 start_camera4 start_camera5 start_camera6
restart_cameras: restart_camera1 restart_camera2 restart_camera3 restart_camera4 restart_camera5 restart_camera6
update_cameras: update_camera1 update_camera2 update_camera3 update_camera4 update_camera5 update_camera6

upload: upload_controller upload_camera
restart: restart_controller restart_camera

deploy_camera1: upload_camera1 restart_camera1
deploy_camera2: upload_camera2 restart_camera2
deploy_camera3: upload_camera3 restart_camera3
deploy_camera4: upload_camera4 restart_camera4
deploy_camera5: upload_camera5 restart_camera5
deploy_camera6: upload_camera6 restart_camera6

deploy_controller: upload_controller restart_controller
deploy_cameras: deploy_camera1 deploy_camera2 deploy_camera3 deploy_camera4 deploy_camera5 deploy_camera6

deploy: upload restart
