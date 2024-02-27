# Project Op Cit
This is a plugin for the [Crossref Labs API](https://gitlab.com/crossref/labs/lambda-api-proxy) that allows for the automatic digital preservation deposit of incoming XML.

![Op Cit Logo](https://gitlab.com/crossref/labs/opcit/-/raw/main/opcit/logo/logo-large.png)

![license](https://img.shields.io/gitlab/license/crossref/labs/opcit) ![activity](https://img.shields.io/gitlab/last-commit/crossref/labs/opcit) <a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>

![FastAPI](https://img.shields.io/badge/fastapi-%23092E20.svg?style=for-the-badge&logo=fastapi&logoColor=white) ![Git](https://img.shields.io/badge/git-%23F05033.svg?style=for-the-badge&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white) ![Linux](https://img.shields.io/badge/Linux-FCC624?style=for-the-badge&logo=linux&logoColor=black) ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

The application examines incoming XML deposits, checks for openly licensed material, and deposits it in an extensible range of digital preservation archives.

## Installation
The easiest install is via pip:
    
    pip install opcit

The entry point is the main deposit function, which takes a StarletteRequest object and a [longsight Instrumentation logging object](https://gitlab.com/crossref/labs/longsight).

## Background
[Project Op Cit](https://www.crossref.org/blog/a-request-for-comment-automatic-digital-preservation-and-self-healing-dois/) is _an experimental technology_ that  replaces the conventional Crossref deposit workflow with a new process that includes digital preservation. The application is designed to be called from the Crossref Labs API, and is not intended to be run as a standalone application.

The workflow for the application is as follows:

1. The Crossref Labs API receives a deposit request.
2. The Crossref Labs API calls the `deposit` function in the `opcit` package.
3. The `deposit` function checks the incoming XML for openly licensed material.
4. If openly licensed material is found, the `deposit` function deposits the material in a digital preservation archive.
5. The `deposit` function returns a response to the Crossref Labs API, which replaces the user's resource URL with an additional resource URL for the preserved version. This triggers [Chooser](https://gitlab.com/crossref/chooser) for [multiple resolution](https://www.crossref.org/documentation/register-maintain-records/creating-and-managing-dois/multiple-resolution/). An example of such a landing page can be seen at https://doi.org/10.32013/12345678-23.
6. The Crossref Labs API returns a response to the original deposit request.

This can be visualized as follows:

![Op Cit Workflow](https://gitlab.com/crossref/labs/opcit/-/raw/main/opcit/logo/deposit-process-blog.png)

![Op Cit Workflow](https://gitlab.com/crossref/labs/opcit/-/raw/main/opcit/logo/resolution-process-blog.png)

At present, Op Cit will only preserve PDF files that are specified in the XML under the `<resource>` element tag. The application will not preserve any other file types, and will not preserve any files that are not specified in the XML.

## Usage

First, ensure that your XML contains a `<resource>` tag with a `mimetype` attribute and a `filename` value. The `mimetype` attribute should contain the MIME type of the file (bearing in mind that only PDFs will be preserved), and the `filename` value should contain the URL of the file. For example:

```
<collection property="crawler-based">
    <item crawler="iParadigms">
        <resource mime_type="application/pdf">https://eprints.bbk.ac.uk/id/eprint/26645/1/9780198850489.pdf</resource>
    </item>
</collection>
```

Second, ensure that your XML contains a `<license>` tag with a `applies_to` attribute and a `href` value. The `applies_to` attribute should contain the version of the file to which the license applies, and the `href` value should contain the URL of the license. Only openly licensed material (using a Creative Commons license) will be deposited. For example:

```
<program xmlns="http://www.crossref.org/AccessIndicators.xsd">
    <free_to_read/>
    <license_ref applies_to="vor" start_date="2022-01-01">https://creativecommons.org/licenses/by/4.0/</license_ref>
</program>
```

Finally, repoint your deposit request to the Op Cit API. The API will return a response with the new URL of the resource, which will trigger multiple resolution and Chooser. The live version of the prototype deposit API can be found at https://api.crossref.org/deposit/preserve/.

POST requests to this URL should conform to [the synchronous deposit API guidelines](https://crossref.gitlab.io/knowledge_base/docs/services/xml-deposit-synchronous-2/).

Please note that Op Cit is not suitable for mass deposits, and is intended for use with individual or small deposits only. Those making larger deposits should continue to use the XML deposit API.

## Disclaimers
This is an experimental technology without guarantee of uptime or reliability and is not intended for production use. The application is not intended to be run as a standalone application, and is designed to be called from the Crossref Labs API. The application is not intended to be used for mass deposits, and is intended for use with individual or small deposits only. Those making larger deposits should continue to use the XML deposit API.

# Credits
* [FastAPI](https://fastapi.tiangolo.com/) for the Crossref Labs API.
* [Git](https://git-scm.com/) from Linus Torvalds _et al_.
* [.gitignore](https://github.com/github/gitignore) from Github.

&copy; Crossref 2023