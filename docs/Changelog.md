# Development Log

- 2026-01-11: Released videofetch v0.5.3 - added two video parsers, namely, CCCVideoClient and MiZhiVideoClient.

- 2026-01-10: Released videofetch v0.5.2 - partial code optimization, supports both direct-link parsing and standard webpage parsing, and adds a unified/general-purpose parsing interface.

- 2026-01-09: Released videofetch v0.5.1 - add three new short-video parsing APIs.

- 2026-01-09: Released videofetch v0.5.0 - refactored the code structure, improved the stability of some video clients, removed deprecated interfaces and paid platforms, and fixed some potential bugs.

- 2026-01-01: Released videofetch v0.4.6 - fix a bug when dealing with special download url type.

- 2026-01-01: Released videofetch v0.4.5 - some argument adjustments, removed the mandatory Playwright import dependency, and rolled back the hostname retrieval method.

- 2025-12-31: Released videofetch v0.4.4 - optimize the iterative-matching approach for the video parser.

- 2025-12-28: Released videofetch v0.4.3 - added native API parsing support for iQIYI and 1905.com, introduced a unified video parsing interface, and made a few minor code optimizations.

- 2025-12-23: Released videofetch v0.4.2 - introduce multiple new parsing endpoints.

- 2025-12-19: Released videofetch v0.4.1 - added support for two general-purpose video parsing and downloading platforms, as well as one specific platform’s video parsing and downloading, and optimized the parsing and downloading for Xigua videos.

- 2025-12-17: Released videofetch v0.4.0 - support parsing for more platforms; automatically enable N_m3u8DL-RE acceleration for all m3u8/HLS streams; and fix some bugs.

- 2025-12-15: Released videofetch v0.3.9 - supports the SnapWC universal parsing API, and updated the CCTV M3U8 downloader to use N_m3u8DL-RE instead of the previous solution.

- 2025-12-15: Released videofetch v0.3.8 - remove the general parsing endpoints that have switched to paid access, and add two free general parsing endpoints and make some improvements.

- 2025-12-12: Released videofetch v0.3.7 - add one general-purpose video parsing client.

- 2025-12-12: Released videofetch v0.3.6 - add two general-purpose video parsing clients.

- 2025-12-12: Released videofetch v0.3.5 - added support for parsing on two specific platforms and introduced a generic parsing interface.

- 2025-12-11: Released videofetch v0.3.4 - fix the problems with downloading CCTV videos.

- 2025-12-08: Released videofetch v0.3.3 - some simple code fixes, and a generic xiami parsing interface has been added.

- 2025-12-06: Released videofetch v0.3.2 - added a new generic parsing interface, support for parsing two specific websites, and special handling of Base64 encoding in parts of the generic parser.

- 2025-12-06: Released videofetch v0.3.1 - added several general-purpose parsers and made some minor feature improvements.

- 2025-12-05: Released videofetch v0.3.0 - add support for more sites and introduce features of the generic parser to help enable parsing across the entire web.

- 2025-11-29: Released videofetch v0.2.3 - add support for `FoxNewsVideoClient` and `SinaVideoClient`, and introduce N_m3u8DL-RE to improve the download speed of HLS/m3u8 streams.

- 2025-11-28: Released videofetch v0.2.2 - added video parsing support for multiple platforms, and fixed a multithreading bug in the download progress bar along with several minor issues.

- 2025-11-26: Released videofetch v0.2.1 - add/fix support for more video platforms and perform some code optimizations.

- 2025-11-21: Released videofetch v0.2.0 - code refactored and extensive support added for downloading videos from many additional platforms.

- 2022-07-19: Released videofetch v0.1.9 — fixed download sources for TED and Douyin videos.

- 2022-03-23: Released videofetch v0.1.8 — optimized the downloader progress bar and added support for YinYueTai, Weibo, Baidu Tieba, Kuaishou Video, Ku6, and Sohu TV.

- 2022-03-08: Released videofetch v0.1.7 — added support for using the `-i` option with the `videodl` command to specify video URLs directly in the terminal.

- 2022-03-02: Released videofetch v0.1.6 — enabled running the tool directly via the `videodl` terminal command.

- 2022-02-17: Released videofetch v0.1.5 — added support for PiPiXia, PiPiGaoXiao, and TED videos.

- 2022-01-05: Released videofetch v0.1.4 — fixed an issue where long videos from iQIYI and Mango TV could not be downloaded.

- 2022-01-04: Released videofetch v0.1.3 — fixed an issue where some videos from CCTV Video were not fully downloaded.

- 2021-12-27: Released videofetch v0.1.2 — added support for iQIYI and Xigua videos.

- 2021-12-26: Released videofetch v0.1.1 — added support for Zhihu and Bilibili videos.

- 2021-12-22: Released videofetch v0.1.0 — added video downloaders for CCTV Video, Mango TV, Migu Video, AcFun, Douyin, and Haokan Video.