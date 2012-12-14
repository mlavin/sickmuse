STATIC_DIR = ./sickmuse/static


install:
	# Install Bower components
	# Requires bower
	cd ${STATIC_DIR} && bower install


build-css:
	# Build CSS from LESS
	# Requires LESS
	# Copy font-awesome fonts
	mkdir -p ${STATIC_DIR}/fonts/
	cp ${STATIC_DIR}/libs/font-awesome/font/* ${STATIC_DIR}/fonts/
	lessc -x ${STATIC_DIR}/less/sickmuse.less ${STATIC_DIR}/css/sickmuse.css
