
run-container:
	make BuildImage
	docker-compose up -d

BuildImage:
	chmod +x start.sh etcd etcdctl
	docker build -t msb_etcd:v1.0 .


