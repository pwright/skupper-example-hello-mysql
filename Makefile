
.PHONY: build-images
build-images:
	cd frontend && make build

# Prerequisite: podman login quay.io
.PHONY: push-images
push-images: build-images
	cd frontend && make push

.phony: clean
clean:
	rm -rf scripts/__pycache__
	rm -f README.html

README.html: README.md
	pandoc -o $@ $<
