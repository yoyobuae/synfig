# $Id$

PLUGIN_NAME = tgs-exporter

plugindir = ${datadir}/synfig/plugins/$(PLUGIN_NAME)
plugin_DATA = \
			  $(PLUGIN_NAME).py \
			  plugin.xml

@INTLTOOL_XML_RULE@

EXTRA_DIST = \
	$(PLUGIN_NAME).py \
	plugin.xml.in

MAINTAINERCLEANFILES = Makefile.in
DISTCLEANFILES = plugin.xml
