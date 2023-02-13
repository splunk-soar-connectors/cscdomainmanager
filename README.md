[comment]: # "Auto-generated SOAR connector documentation"
# CSC DomainManager

Publisher: Splunk Community  
Connector Version: 1\.0\.1  
Product Vendor: Corporation Services Company  
Product Name: CSC Domain Manager  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 5\.4\.0  

Connects to CSC Domain manager platform using CSC Domain manager API services

[comment]: # "File: README.md"
[comment]: # "Copyright (c) Splunk, 2023 Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
## [CSC Domain Manager API](https://www.cscglobal.com/cscglobal/docs/dbs/domainmanager/api-v2/#/)

### Actions Configured

-   [get all
    domains](https://www.cscglobal.com/cscglobal/docs/dbs/domainmanager/api-v2/#/domains/get_domains)
-   [get specific
    domain](https://www.cscglobal.com/cscglobal/docs/dbs/domainmanager/api-v2/#/domains/get_domains__qualifiedDomainName_)
-   [check domain
    available](https://www.cscglobal.com/cscglobal/docs/dbs/domainmanager/api-v2/#/domains/get_domains_availability)
-   [register
    domain](https://www.cscglobal.com/cscglobal/docs/dbs/domainmanager/api-v2/#/domains/post_domains_registration)

### Important Notes

-   If you want to register domains, perhaps for buying up typo squat opportunities, you'll need
    your CSC Account number.


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a CSC Domain Manager asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**endpoint\_url** |  optional  | string | CSC endpoint url
**accountNumber** |  required  | numeric | CSC account number
**apikey** |  required  | password | API key for authentication
**bearer\_token** |  required  | password | Bearer token that accompanies API key for authentication

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[get all domains](#action-get-all-domains) - Get all domain portfolio data  
[get specific domain](#action-get-specific-domain) - Get domain data by qualified domain name  
[check domain available](#action-check-domain-available) - Check registration availability for one or more domain names  
[register domain](#action-register-domain) - Place a domain registration order  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'get all domains'
Get all domain portfolio data

Type: **investigate**  
Read only: **True**

By default, pull first page of domains found in the account \(15000 by default\)\.  If provided, filter parameter can limit the search results\.

<a href="https\://www\.cscglobal\.com/cscglobal/docs/dbs/domainmanager/api\-v2/\#/domains/get\_domains">Link to CSC documentation, for reference</a>\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**selector** |  optional  | The attribute of the domain to search with\.  For example, "qualifiedDomainName=like='example\\\*'" or "nameservers=in=\('dns1\.mydns\.com', 'dns2\.mydns\.com'\)" | string |  `csc domain selector` 
**operator** |  optional  | Search operators used to clarify selector\.  == for Equals, =gt= for Greater Than, =le= for Less Than or Equal To, etc\. | string | 
**value** |  optional  | Value to compare to selector based on operator\.  For example, "filter=qualifiedDomainName==\{value\}" | string | 
**sort** |  optional  | Specify how results should be sorted\:  Ex\:  propertyName,\(desc\|asc\) | string | 
**custom** |  optional  | For custom or more complex searches that use joiner values | string | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |  
action\_result\.parameter\.custom | string |  |  
action\_result\.parameter\.operator | string |  |  
action\_result\.parameter\.selector | string |  `csc domain selector`  |  
action\_result\.parameter\.sort | string |  |  
action\_result\.parameter\.value | string |  |  
action\_result\.data | string |  |  
action\_result\.summary | string |  |  
action\_result\.message | string |  |  
summary\.total\_objects | numeric |  |  
summary\.total\_objects\_successful | numeric |  |    

## action: 'get specific domain'
Get domain data by qualified domain name

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**fqdn** |  required  | Qualified domain name | string |  `domain` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |  
action\_result\.parameter\.fqdn | string |  `domain`  |  
action\_result\.data | string |  |  
action\_result\.summary | string |  |  
action\_result\.message | string |  |  
summary\.total\_objects | numeric |  |  
summary\.total\_objects\_successful | numeric |  |    

## action: 'check domain available'
Check registration availability for one or more domain names

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**fqdn** |  required  | Values of one or more domains to check for availability, separated by a comma\.  Max 50 domains in one query\. | string |  `domain` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |  
action\_result\.parameter\.fqdn | string |  `domain`  |  
action\_result\.data | string |  |  
action\_result\.summary | string |  |  
action\_result\.message | string |  |  
summary\.total\_objects | numeric |  |  
summary\.total\_objects\_successful | numeric |  |    

## action: 'register domain'
Place a domain registration order

Type: **generic**  
Read only: **False**

If an order template is available for the account mapped to the bearer token, then only the "qualifiedDomainName" property is required\.  Otherwise, the request is built with the values provided in the fields below\.

\[Link to CSC Documentation\]\(https\://www\.cscglobal\.com/cscglobal/docs/dbs/domainmanager/api\-v2/\#/domains/post\_domains\_registration\)\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**qualifieddomainname** |  required  | Domain to register | string |  `domain` 
**businessunit** |  required  | Business Unit abbreviation to use in domain registration\. | string | 
**term** |  optional  | Term, in months, to register domain\.  Defaults to 12 months\. | string | 
**brand** |  optional  | Brand name value to provide in domain registration\.  Defaults to empty string\. | string | 
**registrantprofile** |  required  | Value to list as whois contact\.  Must exist already in CSC or order will be incomplete\. | string | 
**adminprofile** |  required  | Value to list as whois contact\.  Must exist already in CSC or order will be incomplete\. | string | 
**technicalprofile** |  required  | Value to list as whois contact\.  Must exist already in CSC or order will be incomplete\. | string | 
**nameservers** |  required  | Comma\-separated string of name servers to use in registration\.  Only required if there is no order template mapped to your bearer token\. | string | 
**dnstype** |  optional  | Type of DNS configuration\.  Defaults to CSC\_BASIC\. | string | 
**notes** |  optional  | Notes to provide in registration payload\.  Defaults to "Registered by Security Automation" if not provided\. | string | 
**notificationsenabled** |  optional  | Whether or not email notifications are enabled for domain registration\.  Defaults to False\. | boolean | 
**additionalnotificationemails** |  optional  | Comma\-separated string of email addresses to add as receivers of notifications related to this domain\. | string | 
**redactpublicwhois** |  optional  | Whether to anonymize public whois info\.  Defaults to False\. | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action\_result\.status | string |  |  
action\_result\.parameter\.additionalnotificationemails | string |  |  
action\_result\.parameter\.adminprofile | string |  |  
action\_result\.parameter\.brand | string |  |  
action\_result\.parameter\.businessunit | string |  |  
action\_result\.parameter\.dnstype | string |  |  
action\_result\.parameter\.nameservers | string |  |  
action\_result\.parameter\.notes | string |  |  
action\_result\.parameter\.notificationsenabled | boolean |  |  
action\_result\.parameter\.qualifieddomainname | string |  `domain`  |  
action\_result\.parameter\.redactpublicwhois | boolean |  |  
action\_result\.parameter\.registrantprofile | string |  |  
action\_result\.parameter\.technicalprofile | string |  |  
action\_result\.parameter\.term | string |  |  
action\_result\.data | string |  |  
action\_result\.summary | string |  |  
action\_result\.message | string |  |  
summary\.total\_objects | numeric |  |  
summary\.total\_objects\_successful | numeric |  |  