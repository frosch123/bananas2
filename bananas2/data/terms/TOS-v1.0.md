# Terms of Service
Version 1.2, 2010-01-26

1. You will only upload content of which you are (one of) the original author(s).

2. You grant the OpenTTD team the rights to distribute the last version of your content from a central server. We will assign a globally unique identifier to each upload and everyone can download the content when they know that identifier.

3. You grant the OpenTTD team to distribute your latest content via our website.

4. You grant the OpenTTD team to retain older versions of your content for the purpose of loading save games with said older version.

5. You grant the OpenTTD team the rights to distribute your content from a central server when specifically asked for it by its unique identifier and MD5 checksum. The origin of the unique identifier and MD5 checksum differs per type of content:

    (a) Base graphics: unique identifier is constructed from the four character short name defined in the .obg file. The MD5 checksum is the exclusive or of the MD5 checksum of the 6 GRFs that are part of the graphics pack.

    (b) NewGRFs: unique identifier is constructed from the GRF ID. The MD5 checksum is the MD5 checksum of the .grf file.

    (c) AIs and AI Libraries: unique identifier is constructed from the four character short name defined in the info.nut. The MD5 checksum is the exclusive or of the MD5 checksums of all scripting files that are part of the AI or AI Library.

    (d) Heightmaps and scenarios: unique identifier is automatically generated when you upload the content. The MD5 checksum is the MD5 checksum of the scenario/heightmap.

    (e) Base sound: unique identifier is constructed from the four character short name defined in the .obs file. The MD5 checksum is the MD5 checksum of the cat file that is part of the sound pack.

    (f) Base music: unique identifier is constructed from the four character short name defined in the .obm file. The MD5 checksum is the exclusive or of MD5 checksum of the music files that are part of the music pack. If they are mentioned multiple times in the .obm file they are exclusive or-ed multiple times.

6. You grant the OpenTTD team the rights to repackage your content before publishing it. The repackaging:

    (a) keeps files called "readme", "license" and "copying" with .txt or .pdf as extension or without an extension.

    (b) requires a "license" or "copying" file in the package file or requires that you selected a non-custom license when uploading the package. In the latter case that license will be added to the package.

    (c) renames files called "copying" to "license" retaining the extension.

    (d) requires exactly one .grf file in NewGRF packages.

    (e) requires exactly one .obg file and exactly six .grf files in Base graphics packages as named in the .obg file and with the same MD5 checksums as defined in the .obg file.

    (f) requires .nut files in AI and AI Library packages.

    (g) changes newlines from .txt files to "DOS" (\r\n) newlines.

    (h) changes newlines from .nut, .obg and .obs files to "unix" (\n) newlines.

    (i) requires a "main.nut" and "info.nut" in AI packages.

    (j) requires a "main.nut" and "library.nut" in AI Library packages.

    (k) requires exactly one .scn or one .sv0 or one .ss0 file in Scenario packages.

    (l) requires exactly one .png or one .bmp file in Heightmap packages.

    (m) requires exactly one .obs file and exactly one .cat file in Base sound packages as named in the .obs file and with the same MD5 checksum as defined in the .obs file.

    (n) requires exactly one .obm file and a number of music files in Base music packages as named in the .obm file and with the same MD5 checksum as defined in the .obm file.
