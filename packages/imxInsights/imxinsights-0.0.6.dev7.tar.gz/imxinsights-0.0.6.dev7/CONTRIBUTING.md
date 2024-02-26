# Contributing to ImxInsights

First off, ❤️ ️ ️thanks for taking the time to contribute! ❤️

All types of contributions are encouraged and valued!!! Please make sure to read the relevant section before making your contribution. 
It will make it a lot easier for us maintainers and smooth out the experience for all involved. The community looks forward to your contributions.

>  🎉 And if you like the project, but just don't have time to contribute, that's fine. There are other easy ways to support the project and show your appreciation, which we would also be very happy about:
> - Star the project
> - Tweet about it
> - Refer this project in your project's readme
> - Mention the project at local meetups and tell your friends/colleagues


### Requirements
We use a `pyproject.toml` to manage requirements that can be build by a newer build backend.
run `pip install .[dev, mkdocs]` or leave out any dependency option you want.

For now we use flit as a build-backend and for managing (optional) dependencies, we are planning to migrate to hatch and for linting to ruff to gain some rust speed on linting.

### Installation
todo
 - make install
 - optional dependency

### Build and Test
Code quality checks and testing needs to be passed and will be checked by a git pre hook on every commit and in the pipeline. 
If code wont pass it won't commit! (warning stil a todo!)

Git-hooks will be set by pre-commit framework, adjust .pre-commit-config.yaml and make sure to install `pre-commit install` after adjustment. (warning stil a todo!)

We use `make` for quality of life: 

- pytest for testing, manual by `make test` in a console.
- flake8 and black for linting, manual by `make lint` in a console*. 
- mypy for typechecking, manual by `make typecheck` in a console.
- isort for sorting imports, manual by `make format` in a console.


## I Have a Question

> If you want to ask a question, we assume that you have read the available [Documentation](https://github.com/Hazedd/imxInsightsCore).

Before you ask a question, it is best to search for existing [Issues](https://github.com/Hazedd/imxInsightsCore/issues) that might help you. In case you have found a suitable issue and still need clarification, you can write your question in this issue. It is also advisable to search the internet for answers first.

If you then still feel the need to ask a question and need clarification, we recommend the following:

- Open an [Issue](https://github.com/Hazedd/imxInsightsCore/issues/new).
- Provide as much context as you can about what you're running into.
- Provide project and platform versions (nodejs, npm, etc), depending on what seems relevant.

We will then take care of the issue as soon as possible.


## I Want To Contribute

> ### Legal Notice <!-- omit in toc -->
> When contributing to this project, you must agree that you have authored 100% of the content, that you have the necessary rights to the content and that the content you contribute may be provided under the project licence.

Make an effort to test each bit of functionality you add. Try to keep it simple. But first we need to add missing test and refactor code. 

The library will be used by end users so every public methode and class should have doc strings and examples. We use mkdocs to manage and publish documentation, we plan to make md files after finshing the alpha release.

## Design
<!-- TODO -->

## CI-CD github workflow

### Identify and Plan Features
- **Gather requirements:** Understand what features your users or stakeholders need.
- **Prioritize:** Determine which features are most important and should be implemented first.
- **Break down:** If a feature is large, consider breaking it down into smaller, manageable tasks.

### Create a Feature Branch
- For each feature, create a new branch from the `master` branch.
- Use a descriptive name for the branch, such as `feature/new-feature-name`.

### Implement the Feature
- **Write code:** Develop the functionality according to the defined requirements.
- **Follow best practices:** Write clean, maintainable code and adhere to coding standards.
- **Write tests:** Create tests to ensure the feature works as expected and to prevent regressions.

### Test the Feature
- Test the feature thoroughly to identify and fix any bugs or issues.
- Include unit tests, integration tests, and if applicable, end-to-end tests.

### Review and Iterate
- If you're working in a team, have your code reviewed by peers.
- Incorporate feedback and make necessary adjustments to the feature implementation.

### Merge Feature Branch
- Once the feature is complete and tested, merge the feature branch into the `main` branch.
- Resolve any merge conflicts if they occur.

### Update Documentation
- Update documentation, such as README.md, to reflect the new feature.
- Include any relevant information on how to use the feature, configuration options, or changes to existing functionalities.

### Release
- If appropriate, tag a release to mark the inclusion of the new feature.
- Communicate the release notes to users or stakeholders.

### Monitor and Collect Feedback
- Monitor the feature in production to ensure it performs as expected.
- Gather feedback from users and stakeholders to iterate on the feature if necessary.


### Versioning
This library follows Semantic Versioning, every successful PR results in a new build version. Version can have a dev, alpha or beta releases state.

We use bumpversion for changing the version, version can be found in the `setting.cfg` and the `__init__.py` of the pyImx module:

  - bumpversion-build, manual and in (nightly) build `make bumpversion-build`
  - bumpversion-patch, manual `make bumpversion-patch`
  - bumpversion-minor, manual `make bumpversion-minor`
  - bumpversion-major, manual `make bumpversion-major`


## Reporting Bugs

### Before Submitting a Bug Report

A good bug report shouldn't leave others needing to chase you up for more information. Therefore, we ask you to investigate carefully, collect information and describe the issue in detail in your report. Please complete the following steps in advance to help us fix any potential bug as fast as possible.

- Make sure that you are using the latest version.
- Determine if your bug is really a bug and not an error on your side e.g. using incompatible environment components/versions (Make sure that you have read the [documentation](https://github.com/Hazedd/imxInsightsCore). If you are looking for support, you might want to check [this section](#i-have-a-question)).
- To see if other users have experienced (and potentially already solved) the same issue you are having, check if there is not already a bug report existing for your bug or error in the [bug tracker](https://github.com/Hazedd/imxInsightsCore/issues?q=label%3Abug).
- Also make sure to search the internet (including Stack Overflow) to see if users outside of the GitHub community have discussed the issue.
- Collect information about the bug:
  - Stack trace (Traceback)
  - OS, Platform and Version (Windows, Linux, macOS, x86, ARM)
  - Version of the interpreter, compiler, SDK, runtime environment, package manager, depending on what seems relevant.
  - Possibly your input and the output
  - Can you reliably reproduce the issue? And can you also reproduce it with older versions?

### How Do I Submit a Good Bug Report?

> You must never report security related issues, vulnerabilities or bugs including sensitive information to the issue tracker, or elsewhere in public. Instead sensitive bugs must be sent by email to <>.
<!-- You may add a PGP key to allow the messages to be sent encrypted as well. -->

We use GitHub issues to track bugs and errors. If you run into an issue with the project:

- Open an [Issue](https://github.com/Hazedd/imxInsightsCore/issues/new). (Since we can't be sure at this point whether it is a bug or not, we ask you not to talk about a bug yet and not to label the issue.)
- Explain the behavior you would expect and the actual behavior.
- Please provide as much context as possible and describe the *reproduction steps* that someone else can follow to recreate the issue on their own. This usually includes your code. For good bug reports you should isolate the problem and create a reduced test case.
- Provide the information you collected in the previous section.

Once it's filed:

- The project team will label the issue accordingly.
- A team member will try to reproduce the issue with your provided steps. If there are no reproduction steps or no obvious way to reproduce the issue, the team will ask you for those steps and mark the issue as `needs-repro`. Bugs with the `needs-repro` tag will not be addressed until they are reproduced.
- If the team is able to reproduce the issue, it will be marked `needs-fix`, as well as possibly other tags (such as `critical`), and the issue will be left to be [implemented by someone](#your-first-code-contribution).

<!-- You might want to create an issue template for bugs and errors that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->


### Suggesting Enhancements

This section guides you through submitting an enhancement suggestion for ImxInsights, **including completely new features and minor improvements to existing functionality**. Following these guidelines will help maintainers and the community to understand your suggestion and find related suggestions.


#### Before Submitting an Enhancement

- Make sure that you are using the latest version.
- Read the [documentation](https://github.com/Hazedd/imxInsightsCore) carefully and find out if the functionality is already covered, maybe by an individual configuration.
- Perform a [search](https://github.com/Hazedd/imxInsightsCore/issues) to see if the enhancement has already been suggested. If it has, add a comment to the existing issue instead of opening a new one.
- Find out whether your idea fits with the scope and aims of the project. It's up to you to make a strong case to convince the project's developers of the merits of this feature. Keep in mind that we want features that will be useful to the majority of our users and not just a small subset. If you're just targeting a minority of users, consider writing an add-on/plugin library.


#### How Do I Submit a Good Enhancement Suggestion?

Enhancement suggestions are tracked as [GitHub issues](https://github.com/Hazedd/imxInsightsCore/issues).

- Use a **clear and descriptive title** for the issue to identify the suggestion.
- Provide a **step-by-step description of the suggested enhancement** in as many details as possible.
- **Describe the current behavior** and **explain which behavior you expected to see instead** and why. At this point you can also tell which alternatives do not work for you.
- You may want to **include screenshots or screen recordings** which help you demonstrate the steps or point out the part which the suggestion is related to. You can use [LICEcap](https://www.cockos.com/licecap/) to record GIFs on macOS and Windows, and the built-in [screen recorder in GNOME](https://help.gnome.org/users/gnome-help/stable/screen-shot-record.html.en) or [SimpleScreenRecorder](https://github.com/MaartenBaert/ssr) on Linux. <!-- this should only be included if the project has a GUI -->
- **Explain why this enhancement would be useful** to most ImxInsights users. You may also want to point out the other projects that solved it better and which could serve as inspiration.

<!-- You might want to create an issue template for enhancement suggestions that can be used as a guide and that defines the structure of the information to be included. If you do so, reference it here in the description. -->

### Your First Code Contribution
<!-- TODO
include Setup of env, IDE and typical getting started instructions?

-->

### Improving The Documentation
<!-- TODO
Updating, improving and correcting the documentation

-->

## Styleguides
### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 72 characters or less
* Reference issues and pull requests liberally after the first line
* When only changing documentation, include `[ci skip]` in the commit title
* Consider starting the commit message with an applicable emoji:
    * :art: `:art:` when improving the format/structure of the code
    * :racehorse: `:racehorse:` when improving performance
    * :non-potable_water: `:non-potable_water:` when plugging memory leaks
    * :memo: `:memo:` when writing docs
    * :bug: `:bug:` when fixing a bug
    * :fire: `:fire:` when removing code or files
    * :green_heart: `:green_heart:` when fixing the CI build
    * :white_check_mark: `:white_check_mark:` when adding tests
    * :lock: `:lock:` when dealing with security
    * :arrow_up: `:arrow_up:` when upgrading dependencies
    * :arrow_down: `:arrow_down:` when downgrading dependencies
    * :shirt: `:shirt:` when removing linter warnings


## Join The Project Team
<!-- TODO -->


## Attribution
This guide is based on the **contributing-gen**. [Make your own](https://github.com/bttger/contributing-gen)!


## Code of Conduct

This project and everyone participating in it is governed by the
[ImxInsights Code of Conduct](https://github.com/Hazedd/imxInsightsCore/blob/master/CODE_OF_CONDUCT.md).
By participating, you are expected to uphold this code. Please report unacceptable behavior
to <>.
