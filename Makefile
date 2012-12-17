STATIC_DIR = ./sickmuse/static


install-static:
	# Install Bower components
	# Requires bower
	cd ${STATIC_DIR} && bower install


build-css:
	# Build CSS from LESS
	# Requires LESS
	# Copy font-awesome fonts
	mkdir -p ${STATIC_DIR}/fonts/
	cp ${STATIC_DIR}/libs/font-awesome/font/* ${STATIC_DIR}/font/
	lessc -x ${STATIC_DIR}/less/sickmuse.less ${STATIC_DIR}/css/sickmuse.css


build-js:
	# Build optimized JS
	# Requires r.js
	cd ${STATIC_DIR}/js && r.js -o name=sickmuse out=sickmuse-built.js baseUrl=. mainConfigFile=sickmuse.js


lint-js:
	# Check JS for any problems
	jshint ${STATIC_DIR}/js/sickmuse.js
	jshint ${STATIC_DIR}/js/models/host-plugin.js
	jshint ${STATIC_DIR}/js/views/plugin-graph.js
