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
* User roles and global moderators
* Moderator-defined label/categories for content
* Comment/feedback/rating functions
* More meta-information for content

## Minor goals
* Detect dependencies of scenarios
* Allow renaming content
* Allow updating meta data and readmes of any version, without uploading a new version of the content itself.
* All texts can make use of Markdown
* Screenshots for NewGRF, scenarios, heightmap preview
* Source bundles for projects with OSS licence
* Access readme, licence, changelog, ... without downloading the content.
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

Bananas allows downloading any version if you know the checksum. For example if you need a specific version for loading a savegame.
But when not looking for a specific version, currently only the latest version is actively offered for download.

Project moderators can define which versions are actively offered for download:
* Versions can be tagged as "experimental", "stable", "archived" and "not available".
** "experimental" and "archived" versions are only displayed to users which want to see them.
** "not available" versions are not shown to new users, and are only available when needed for a specific savegame.
* Versions can be set to require certain versions of OpenTTD, or even specific forks/patches.
* By default users are offered the latest "stable" or "archived" version, that is available for their version of OpenTTD:
* The intention of "not available" is to hide buggy versions for users which are unable to use the latest version, and redirect them to an even older but less buggy version.

Possibly also allow defining "branches" for content, so you can have different versions for "official OpenTTD" and "patchpack x".

## Offer stripped versions of NewGRF without 32bpp or without 4x zoom

By default NewGRF containing 32bpp or 4x zoom sprites are also offered as 8bpp-only or 1x-zoom-only versions.
Project moderators can disable 8bpp-only versions, if the NewGRF only contains placeholder sprites.

## User roles and global moderators

* User: Can view public stuff and comment/rate.
* Project moderator: Can edit/organise descriptions/labels for projects, edit version availability and upload new versions.
* Project owner: Can appoint project moderators and owners.
* Global moderator/curator: Can edit/organise descriptions/labels for projects and down-grade availability. (possibly limited by project owners)
* Administrator: Can appoint global moderators and administrators.

The goal is that global moderators
* make the content navigatable,
* make it harder to find buggy/unmaintained content,
* unify usage of labels and descriptions.

Project moderators can specify their position on what global moderators are welcome to do, like
* global moderators are allowed to add/remove labels
* global moderators are allowed to edit the descriptions

Essentially: Project moderators can allow or deny global moderators to edit specific meta data.
The only option they can not deny: Global moderators can always make content more hidden, by setting it to "experimental" or "unavailable".

## Moderator-defined label/categories for content

Global moderators can define new labels and categories, which can be assigned to projects.
This is accompanied by various views which allow browsing the content by label.

This task is a success, when it is unnecessary to maintain manual/external lists like https://wiki.openttd.org/NewGRF_List

## Comment/feedback/rating functions

Users can comment and rate projects and specific versions.
By default only the latest N comments and ratings are considered for rating the project overall.
Project moderators can disable comments and/or ratings for their project, if they feel like it.

## More meta-information for content

Rework the old "tags" system into something more useable by making categories/labels more explicit.
The offered categories and columns are defined/extendible by global moderators.

* Map size for scenarios and heightmaps
* Content types for NewGRF: Vehicles, Industries, ...
* Content scale: "Single-item" vs. "full-features NewGRF set"
* Other categories: Themed for competitive play, themed for transport madness, themed for specific country, ...
* More detailed credits: Distinguish authors, contributors, meta-data moderators, ...
* More URLs for projects: Homepage, source, forum
