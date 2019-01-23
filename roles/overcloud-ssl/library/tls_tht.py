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
        tmp_dict = yaml.safe_load(stream)
    return tmp_dict


def create_enable_file(certpem, keypem, source_dir, dest_dir, tht_release):
    # environments/ssl/* is preferred starting with pike
    if tht_release in ['mitaka', 'newton', 'ocata']:
        output_dict = _open_yaml("{}environments/enable-tls.yaml".format(source_dir))
    else:
        output_dict = _open_yaml("{}environments/ssl/enable-tls.yaml".format(source_dir))

    if tht_release == 'mitaka':
        for key in output_dict["parameter_defaults"]["EndpointMap"]:
            if output_dict["parameter_defaults"]["EndpointMap"][key]["host"] == "CLOUDNAME":
                output_dict["parameter_defaults"]["EndpointMap"][key]["host"] = "IP_ADDRESS"

    output_dict["parameter_defaults"]["SSLCertificate"] = certpem
    output_dict["parameter_defaults"]["SSLKey"] = keypem

    # NoteTLSData has been deprecated/removed in rocky and onwards
    if tht_release in ['mitaka', 'newton', 'ocata', 'pike', 'queens']:
        output_dict["resource_registry"]["OS::TripleO::NodeTLSData"] = \
            "{}/puppet/extraconfig/tls/tls-cert-inject.yaml".format(source_dir)

    with open("{}enable-tls.yaml".format(dest_dir), "w") as stream:
        yaml.safe_dump(output_dict, stream, default_style='|')


def create_anchor_file(cert_ca_pem, source_dir, dest_dir, enable_tls_overcloud):
    output_dict = _open_yaml(
        "{}environments/ssl/inject-trust-anchor.yaml".format(source_dir)
    )

    if enable_tls_overcloud:
        ca_map = {"overcloud-ca": {"content": cert_ca_pem}}
    else:
        ca_map = {}
    # Optionally include the undercloud's local CA certificate
    try:
        undercloud_ca = "/etc/pki/ca-trust/source/anchors/cm-local-ca.pem"
        with open(undercloud_ca, 'ro') as undercloud_ca_file:
            undercloud_ca_content = undercloud_ca_file.read()
        ca_map.update({"undercloud-ca": {"content": undercloud_ca_content}})
    except IOError:
        pass
    output_dict["parameter_defaults"]["CAMap"] = ca_map
    del output_dict["resource_registry"]

    with open("{}inject-trust-anchor.yaml".format(dest_dir), "w") as stream:
        yaml.safe_dump(output_dict, stream, default_style='|')


def main():
    module = AnsibleModule(
        argument_spec=dict(
            enable_tls_overcloud=dict(type="bool", default=False, required=False),
            source_dir=dict(default="/usr/share/openstack-tripleo-heat-templates/",
                            required=False),
            dest_dir=dict(default="", required=False),
            cert_filename=dict(default="cert.pem", required=False),
            cert_ca_filename=dict(default="cert.pem", required=False),
            key_filename=dict(default="key.pem", required=False),
            tht_release=dict(default="master", required=False),
        )
    )

    if module.params["enable_tls_overcloud"]:
        with open(module.params["cert_filename"], "r") as stream:
            certpem = stream.read()

        with open(module.params["key_filename"], "r") as stream:
            keypem = stream.read()
        with open(module.params["cert_ca_filename"], "r") as stream:
            cert_ca_pem = stream.read()

        create_enable_file(certpem, keypem,
                           module.params["source_dir"],
                           module.params["dest_dir"],
                           module.params["tht_release"])
    else:
        cert_ca_pem = None

    create_anchor_file(cert_ca_pem,
                       module.params["source_dir"],
                       module.params["dest_dir"],
                       module.params["enable_tls_overcloud"])
    module.exit_json(changed=True)


if __name__ == '__main__':
    main()
