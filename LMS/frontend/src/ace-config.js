import ace from 'ace-builds';

import modeJsonUrl from 'ace-builds/src-noconflict/mode-json?url';
ace.config.setModuleUrl('ace/mode/json', modeJsonUrl);

import themeMonokaiUrl from 'ace-builds/src-noconflict/theme-monokai?url';
ace.config.setModuleUrl('ace/theme/monokai', themeMonokaiUrl);

import themeOneDarkUrl from 'ace-builds/src-noconflict/theme-one_dark?url';
ace.config.setModuleUrl('ace/theme/one_dark', themeOneDarkUrl);