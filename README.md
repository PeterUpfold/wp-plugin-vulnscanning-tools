# WP Plugin Vulnerability Scanning

## Work in Progress only

Some utilities I'm using to perform some automated vulnerability scanning of WordPress plugins.

## determine-target-plugins.py

 * for each top level plugin slug, pull the https://wordpress.org/plugins/{name} page and parse number of installations
 * Decide which plugins to target based on user base
