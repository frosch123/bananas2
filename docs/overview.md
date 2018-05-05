# Introduction

This document defines goals and details for a new implementation of the OpenTTD content system.
The focus is on reimplementing the web frontend while adding many new features.
The in-game interface shall stay compatible, but won't make use of new features for now.
In-game will follow when the web frontend turns out good.

# Goals

## Major goals

* New content type: OpenTTD patch/patchpack/fork
* New content type: NewGRF preset
* Offer multiple versions of the same content for download
* Offer stripped versions of NewGRF without 32bpp or without 4x zoom
* User roles and global curators
* Curator-defined label/categories for content
* Review/feedback/rating functions
* More meta-information for content

## Minor goals
* Detect dependencies of scenarios
* Allow renaming content
* Allow updating meta data and readmes of any version, without uploading a new version of the content itself.
* All texts can make use of GF-Markdown
* Screenshots for NewGRF, scenarios, heightmap preview
* Source bundles for projects with OSS license
* Access readme, license, changelog, ... without downloading the content.
* Querying usage/availability of unique Ids of NewGRF and AI/GS.


# Details for selected goals

## New content type: OpenTTD patch/patchpack/fork

Bananas will contain binaries and the corresponding source for

* "official" releases, including old ones
* "official" nightly
* patchpacks
* major patches

You cannot just upload any binaries, they must be produced by the OpenTTD compile farm.

The content gets labels and descriptions like every other content on bananas.

* "nightly" are "experimental"
* old "official" releases" are "archived", but still downloadable

For a start the content is only accessible via the bananas web frontend, not in-game :)

## New content type: NewGRF preset

A NewGRF preset is a selection of NewGRF and their parameters.

New versions of the same preset usually contain updated references to the NewGRF versions.

## Offer multiple versions of the same content for download

Bananas allows downloading any version if you know the checksum. For example if you need a specific version for loading a savegame/scenario.
But when not looking for a specific version, currently only the latest version is actively offered for download.

Project editors can define which versions are actively offered for download:

* Versions can be tagged as "experimental", "stable", "archived" and "hidden".
    * "experimental" and "archived" versions are only displayed to users which want to see them.
    * "hidden" versions are not shown to new users, and are only available when needed for a specific savegame/scenario.
* Versions can be set to require certain versions of OpenTTD, or even specific forks/patches.
* By default users are offered the latest "stable" or "archived" version, that is available for their version of OpenTTD:
* The intention of "hidden" is to hide buggy versions for users which are unable to use the latest version, and redirect them to an even older but less buggy version.

Possibly also allow defining "branches" for content, so you can have different versions of a NewGRF for "official OpenTTD" and for "patchpack x".

## Offer stripped versions of NewGRF without 32bpp or without 4x zoom

By default NewGRF containing 32bpp or 4x zoom sprites are also offered as 8bpp-only or 1x-zoom-only versions.
Project editors can disable 8bpp-only versions, if the NewGRF only contains placeholder sprites.

## User roles and global curators

* Banned persons: Treated like anonymous persons.
* Regular users: Can view public stuff and comment/rate.
* Project editors: Can edit/organise descriptions/labels for their projects, edit version availability and upload new versions.
* Project owners: Can appoint project editors and owners in their projects.
* Global curators: Can edit/organise stuff in consent with project owners/editors.
* Global moderators: Moderate general user behaviour independent of any content.
* Administrators: In theory can do everything, but are not supposed to do everything, except on request by the project owner.

The goal is that global curators

* make the content navigatable,
* make it harder to find buggy/unmaintained content,
* unify usage of labels and descriptions.

Project editors can specify their position on what global curators are welcome to do, like

* add/remove labels
* edit the descriptions
* add/organise screenshots
* edit OpenTTD version/fork requirements and compatibility

Essentially: Project editors can allow or deny global curators to edit specific meta data.
The only option they cannot deny: Global curators can always make content more hidden, by setting it to "experimental" or "hidden".

Project editors can also specify whether they welcome regular users to review or rate their projects.

## Curator-defined label/categories for content

Global curators can define new labels and categories, which can be assigned to projects.
This is accompanied by various views which allow browsing the content by label.

This task is a success, when it is unnecessary to maintain manual/external lists like https://wiki.openttd.org/NewGRF_List

## Review/feedback/rating functions

Users can post reviews and rate projects.
By default only the latest N rewiews and ratings are considered for rating the project overall.
Project editors can disable comments and/or ratings for their project, if they feel like it.

## More meta-information for content

Rework the old "tags" system into something more useable by making categories/labels more explicit.
The offered categories and columns are defined/extendible by global curators.

* Map size for scenarios and heightmaps
* Content types for NewGRF: Vehicles, Industries, ...
* Content scale: "Single-item" vs. "full-features NewGRF set"
* Other categories: Themed for competitive play, themed for transport madness, themed for specific country, ...
* More detailed credits: Distinguish authors, contributors, meta-data moderators, ...
* More URLs for projects: Homepage, source, forum
