PROJECT_NAME ?= MID

all:
	@echo "make devenv		- Create & setup development virtual environment"
	@echo "make lint		- Check code with pylama"
	@echo "make postgres	- Start postgres container"
	@echo "make clean		- Remove files created by distutils"
	@echo "make test		- Run tests"
	@echo "make sdist		- Make source distribution"
	@echo "make docker		- Build a docker image"
	@echo "make upload		- Upload docker image to the registry"
	@exit 0

devenv: clean
	rm -rf env
	# создаем новое окружение
	python3.8 -m venv env
	# обновляем pip
	env/bin/pip install -U pip
	# устанавливаем основные + dev зависимости из extras_require (см. setup.py)
	env/bin/pip install -Ue '.[dev]'

dev-pg:
	docker stop mid-postgres || echo No such container: mid-postgres
	docker run --rm --detach --name=mid-postgres \
		--env POSTGRES_USER=user \
		--env POSTGRES_PASSWORD=hackme \
		--env POSTGRES_DB=mid \
		--publish 5432:5432 postgres

# test: lint postgres
# 	env/bin/pytest -vv --cov=analyzer --cov-report=term-missing tests

# docker: sdist
# 	docker build --target=api -t $(PROJECT_NAME):$(VERSION) .

# upload: docker
# 	docker tag $(PROJECT_NAME):$(VERSION) $(REGISTRY_IMAGE):$(VERSION)
# 	docker tag $(PROJECT_NAME):$(VERSION) $(REGISTRY_IMAGE):latest
# 	docker push $(REGISTRY_IMAGE):$(VERSION)
# 	docker push $(REGISTRY_IMAGE):latest