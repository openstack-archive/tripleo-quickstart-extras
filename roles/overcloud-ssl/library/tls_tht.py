#!/usr/bin/python
# coding: utf-8 -*-
#
# (c) 2016, Adriano Petrich <apetrich@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

DOCUMENTATION = '''
---
module: tls_tht
version_added: "1.9"
short_description: Generate the tht templates for enabled ssl
description:
   - Generate the tht templates for enabled ssl
options:
    source_dir:
        description:
            - directory to copy the templates from
        required: false
        default: "/usr/share/openstack-tripleo-heat-templates/"
    dest_dir:
        description:
            - were to copy the files to
        required: false
        default: ""
    cert_filename:
        description:
            - the cert pem filename
        required: false
        default: cert.pem
    cert_ca_filename:
        description:
            - the key pem filename
        required: false
        default: key.pem
    key_filename:
        description:
            - the CA cert pem filename
        required: false
        default: cert.pem
    tht_release:
        description:
            - the tht release name
        required: false
        default: master


'''

EXAMPLES = '''
# Generate the tht templates for enabled ssl
- tls_tht:
'''

import yaml
from ansible.module_utils.basic import *  # noqa


def _open_yaml(filename):
    with open(filename, "r") as stream:
        tmp_dict = yaml.load(stream)
    return tmp_dict


def create_enable_file(certpem, keypem, source_dir, dest_dir, tht_release):
    output_dict = _open_yaml("{}environments/enable-tls.yaml".format(source_dir))

    if tht_release == 'mitaka':
        for key in output_dict["parameter_defaults"]["EndpointMap"]:
            if output_dict["parameter_defaults"]["EndpointMap"][key]["host"] == "CLOUDNAME":
                output_dict["parameter_defaults"]["EndpointMap"][key]["host"] = "IP_ADDRESS"

    output_dict["parameter_defaults"]["SSLCertificate"] = certpem
    output_dict["parameter_defaults"]["SSLKey"] = keypem

    output_dict["resource_registry"]["OS::TripleO::NodeTLSData"] = \
        "{}/puppet/extraconfig/tls/tls-cert-inject.yaml".format(source_dir)

    with open("{}enable-tls.yaml".format(dest_dir), "w") as stream:
        yaml.safe_dump(output_dict, stream, default_style='|')


def create_anchor_file(cert_ca_pem, source_dir, dest_dir):
    output_dict = _open_yaml(
        "{}environments/inject-trust-anchor.yaml".format(source_dir)
    )

    output_dict["parameter_defaults"]["SSLRootCertificate"] = cert_ca_pem

    output_dict["resource_registry"]["OS::TripleO::NodeTLSCAData"] = \
        "{}/puppet/extraconfig/tls/ca-inject.yaml".format(source_dir)

    with open("{}inject-trust-anchor.yaml".format(dest_dir), "w") as stream:
        yaml.safe_dump(output_dict, stream, default_style='|')


def main():
    module = AnsibleModule(
        argument_spec=dict(
            source_dir=dict(default="/usr/share/openstack-tripleo-heat-templates/",
                            required=False),
            dest_dir=dict(default="", required=False),
            cert_filename=dict(default="cert.pem", required=False),
            cert_ca_filename=dict(default="cert.pem", required=False),
            key_filename=dict(default="key.pem", required=False),
            tht_release=dict(default="master", required=False),
        )
    )

    with open(module.params["cert_filename"], "r") as stream:
        certpem = stream.read()

    with open(module.params["cert_ca_filename"], "r") as stream:
        cert_ca_pem = stream.read()

    with open(module.params["key_filename"], "r") as stream:
        keypem = stream.read()

    create_enable_file(certpem, keypem,
                       module.params["source_dir"],
                       module.params["dest_dir"],
                       module.params["tht_release"])
    create_anchor_file(cert_ca_pem,
                       module.params["source_dir"],
                       module.params["dest_dir"])
    module.exit_json(changed=True)


if __name__ == '__main__':
    main()
