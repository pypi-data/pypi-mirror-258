import {
  JupyterFrontEnd
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';

import { PartialJSONObject } from '@lumino/coreutils';

import { find } from '@lumino/algorithm';

import { Widget } from '@lumino/widgets';

import { requestAPI } from './handler';

class DiskSpaceWidget extends Widget {
  constructor(settings: any) {
    super();

    let outerDiv = document.createElement('div')
    outerDiv.className = "diskspace"

    let innerDiv = document.createElement('div')
    innerDiv.className = "diskspace-tooltip-text"

    this.addClass('opensarlab-frontend-object');
    this.node.appendChild(outerDiv);

    const btyes_to_mb = 1.0 / (1024 * 1024)

    checkDiskSpaceInterval(settings)
    setInterval(
      checkDiskSpaceInterval,
      5000,
      settings
    )

    async function checkDiskSpaceInterval (settings: any) {

      let data = await requestAPI<any>('opensarlab-diskspace');
      data = data['data']
  
      const total = data['total']
      const used = data['used']
      const free = data['free']
  
      const percentUsed = used/total * 100
  
      let statusColorClass = ''
      let statusBlinkClass = ''

      let setCriticalThreshold = settings.setCriticalThreshold as number;
      let setDangerThreshold = settings.setDangerThreshold as number;
      let setWarningThreshold = settings.setWarningThreshold as number;
  
      if ( percentUsed >= setCriticalThreshold ) {
        statusColorClass = 'red'
        statusBlinkClass = 'blink-me'
      }
      else if ( percentUsed >= setDangerThreshold ) {
        statusColorClass = 'red'
      }
      else if ( percentUsed >= setWarningThreshold ) {
        statusColorClass = 'yellow'
      }
  
      // span gives disk storage percent remaining
      outerDiv.innerHTML = `
        <span class="${ statusBlinkClass } ${ statusColorClass }">
          Disk space used: ${ percentUsed.toFixed(2).toString() }%
        </span>
      `
  
      // popup gives all the data
      innerDiv.innerHTML = `
        <div> Free MB: ${ (free / btyes_to_mb).toFixed(2) } </div>
        <div> Used MB: ${ (used / btyes_to_mb).toFixed(2) } </div>
        <div> Total MB: ${ (total / btyes_to_mb).toFixed(2) } </div>
      `
      //*** Until the popup renders properly, we are not using it
      /// this.outerDiv.appendChild(this.innerDiv)
    }
  }
}

export async function main(app: JupyterFrontEnd, allSettings: ISettingRegistry.ISettings): Promise<void> {

  const settings = allSettings.get('diskspace').composite as PartialJSONObject ?? allSettings.default('diskspace') as PartialJSONObject;

  let enabled = settings.enabled as boolean;
  let rank = settings.rank as number;

  const widget_id = 'opensarlab-diskspace-widget'

  const widgetPlacement = 'top'

  const widget = find(app.shell.widgets(widgetPlacement), w => w.id === widget_id);
  if (widget) {
      widget.dispose()
  } 

  if(!enabled) {
      console.log('JupyterLab extension opensarlab-frontend:diskspace is not activated!');
      return;
  }

  try {
      const opensarlabdiskspaceSpanWidget = new DiskSpaceWidget(settings);
      opensarlabdiskspaceSpanWidget.id = widget_id;
  
      app.shell.add(opensarlabdiskspaceSpanWidget as any, widgetPlacement, {rank:rank});
  
      console.log('JupyterLab extension opensarlab-frontend:diskspace is activated!');

  } catch (reason) {
      console.error(
          `Error on GET /opensarlab-frontend/opensarlab-diskspace.\n${reason}`
      );
  }
};
