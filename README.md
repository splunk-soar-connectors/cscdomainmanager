# CSC DomainManager

Publisher: Splunk Community \
Connector Version: 1.2.0 \
Product Vendor: Corporation Services Company \
Product Name: CSC Domain Manager \
Minimum Product Version: 5.3.2

Connects to CSC Domain manager platform using CSC Domain manager API services

### Configuration variables

This table lists the configuration variables required to operate CSC DomainManager. These variables are specified when configuring a CSC Domain Manager asset in Splunk SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**endpoint_url** | optional | string | CSC endpoint url |
**accountNumber** | required | numeric | CSC account number |
**apikey** | required | password | API key for authentication |
**bearer_token** | required | password | Bearer token that accompanies API key for authentication |

### Supported Actions

[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration \
[get all domains](#action-get-all-domains) - Get all domain portfolio data \
[get specific domain](#action-get-specific-domain) - Get domain data by qualified domain name \
[check domain available](#action-check-domain-available) - Check registration availability for one or more domain names \
[register domain](#action-register-domain) - Place a domain registration order \
[get order status](#action-get-order-status) - Get one or more orders for a purchase request for a particular fqdn

## action: 'test connectivity'

Validate the asset configuration for connectivity using supplied configuration

Type: **test** \
Read only: **True**

#### Action Parameters

No parameters are required for this action

#### Action Output

No Output

## action: 'get all domains'

Get all domain portfolio data

Type: **investigate** \
Read only: **True**

By default, pull first page of domains found in the account (15000 by default). If provided, filter parameter can limit the search results.

<a href="https://www.cscglobal.com/cscglobal/docs/dbs/domainmanager/api-v2/#/domains/get_domains">Link to CSC documentation, for reference</a>.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**selector** | optional | The attribute of the domain to search with. For example, "qualifiedDomainName=like='example\\\*'" or "nameservers=in=('dns1.mydns.com', 'dns2.mydns.com')" | string | `csc domain selector` |
**operator** | optional | Search operators used to clarify selector. == for Equals, =gt= for Greater Than, =le= for Less Than or Equal To, etc | string | |
**value** | optional | Value to compare to selector based on operator. For example, "filter=qualifiedDomainName=={value}" | string | |
**sort** | optional | Specify how results should be sorted: Ex: propertyName,(desc|asc) | string | |
**custom** | optional | For custom or more complex searches that use joiner values | string | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.data.\*.data.\* | string | `domain` | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |
action_result.parameter.selector | string | `csc domain selector` | |
action_result.parameter.operator | string | | |
action_result.parameter.value | string | | |
action_result.parameter.sort | string | | |
action_result.parameter.custom | string | | |

## action: 'get specific domain'

Get domain data by qualified domain name

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**fqdn** | required | Qualified domain name | string | `domain` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.fqdn | string | `domain` | |
action_result.data | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'check domain available'

Check registration availability for one or more domain names

Type: **investigate** \
Read only: **True**

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**fqdn** | required | Values of one or more domains to check for availability, separated by a comma. Max 50 domains in one query | string | `domain` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.fqdn | string | `domain` | |
action_result.data | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'register domain'

Place a domain registration order

Type: **generic** \
Read only: **False**

If an order template is available for the account mapped to the bearer token, then only the "qualifiedDomainName" property is required. Otherwise, the request is built with the values provided in the fields below.

[Link to CSC Documentation](https://www.cscglobal.com/cscglobal/docs/dbs/domainmanager/api-v2/#/domains/post_domains_registration).

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**qualifieddomainname** | required | Domain to register | string | `domain` |
**businessunit** | required | Business Unit abbreviation to use in domain registration | string | |
**term** | optional | Term, in months, to register domain. Defaults to 12 months | string | |
**brand** | optional | Brand name value to provide in domain registration. Defaults to empty string | string | |
**registrantprofile** | required | Value to list as whois contact. Must exist already in CSC or order will be incomplete | string | |
**adminprofile** | required | Value to list as whois contact. Must exist already in CSC or order will be incomplete | string | |
**technicalprofile** | required | Value to list as whois contact. Must exist already in CSC or order will be incomplete | string | |
**nameservers** | required | Comma-separated string of name servers to use in registration. Only required if there is no order template mapped to your bearer token | string | |
**dnstype** | optional | Type of DNS configuration. Defaults to CSC_BASIC | string | |
**notes** | optional | Notes to provide in registration payload. Defaults to "Registered by Security Automation" if not provided | string | |
**notificationsenabled** | optional | Whether or not email notifications are enabled for domain registration. Defaults to False | boolean | |
**additionalnotificationemails** | optional | Comma-separated string of email addresses to add as receivers of notifications related to this domain | string | |
**redactpublicwhois** | optional | Whether to anonymize public whois info. Defaults to False | boolean | |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.additionalnotificationemails | string | | |
action_result.parameter.adminprofile | string | | |
action_result.parameter.brand | string | | |
action_result.parameter.businessunit | string | | |
action_result.parameter.dnstype | string | | |
action_result.parameter.nameservers | string | | |
action_result.parameter.notes | string | | |
action_result.parameter.notificationsenabled | boolean | | |
action_result.parameter.qualifieddomainname | string | `domain` | |
action_result.parameter.redactpublicwhois | boolean | | |
action_result.parameter.registrantprofile | string | | |
action_result.parameter.technicalprofile | string | | |
action_result.parameter.term | string | | |
action_result.data | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

## action: 'get order status'

Get one or more orders for a purchase request for a particular fqdn

Type: **investigate** \
Read only: **True**

CSC API does not prevent submission of a registration order that is missing fields or has them malformed. This call can help find submissions made that have failed or are held up for some other reason, requiring intervention.

#### Action Parameters

PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**fqdn** | required | The domain which was purchased and is the subject of the query to see the purchase status | string | `domain` |

#### Action Output

DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string | | success failed |
action_result.parameter.fqdn | string | `domain` | |
action_result.data | string | | |
action_result.summary | string | | |
action_result.message | string | | |
summary.total_objects | numeric | | |
summary.total_objects_successful | numeric | | |

______________________________________________________________________

Auto-generated Splunk SOAR Connector documentation.

Copyright 2025 Splunk Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing,
software distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
