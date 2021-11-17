solr_collection
===============

Solr collection creation and management for Solr Cloud with Zookeeper.

Role Variables
--------------

* `solr_server`: server where configset directory will be created, and where zookooper will be run
* `num_shards`: number of shards; default  1
* `replication_factor`: replication factor; default 3
* `shards_per_node`: shards per node; default 1


Example Playbook
----------------

    - hosts: servers
      roles:
         - { role: solr_collection, solr_collection: mycoll, solr_configset: mycfg,        solr_server: solr-staging.ex.co }