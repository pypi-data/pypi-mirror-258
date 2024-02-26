from __future__ import annotations
from typing import TYPE_CHECKING

from functools import total_ordering

from datetime import datetime

from .task import MBIOTask
from .xmlconfig import XMLConfig

import requests
import io
import csv

from prettytable import PrettyTable


@total_ordering
class Trigger(object):
    def __init__(self, dow: str, t: str, state: bool = True, sp=None):
        self._dow=str(dow).lower()
        self._state=bool(state)
        self._sp=sp
        self._h=None
        self._m=None
        self._stamp=None
        self.parseTime(t)

    @property
    def dow(self):
        return self._dow

    @property
    def h(self):
        return self._h

    @property
    def m(self):
        return self._m

    @property
    def stamp(self):
        return self._stamp

    @property
    def state(self):
        return self._state

    @property
    def sp(self):
        return self._sp

    def t(self, offset=0):
        stamp=self.stamp+offset
        return '%02d:%02d' % (stamp // 60, stamp % 60)

    def parseTime(self, t):
        try:
            t=str(t).replace('h', ':')
            if ':' in t:
                items=list(t.split(':'))
                self._h=int(items[0])
                self._m=int(items[1])
                if self._m is None:
                    self._m=0
            else:
                self._h=int(t)
                self._m=0

            self._stamp=self._h*60+self._m
        except:
            pass

    def matchDow(self, date=None):
        try:
            if self._h is not None and self._m is not None:
                if not date:
                    date=datetime.now()
                dow=date.weekday()
                if str(dow) in self._dow:
                    return True
                if '*' in self._dow:
                    return True
                if dow in [6, 7] and self._dow=='we':
                    return True
                if dow<6 and self._dow=='wd':
                    return True
        except:
            pass
        return False

    def __eq__(self, other):
        if self.stamp==other.stamp:
            if self.dow==other.dow:
                return True
        return False

    def __lt__(self, other):
        if self.stamp==other.stamp:
            if self.dow=='*' and other.dow!='*':
                return True
            if self.dow!='*' and other.dow=='*':
                return False
            if len(self.dow)>len(other.dow):
                return True
            return False
        if self.stamp<other.stamp:
            return True
        return False


class Scheduler(object):
    def __init__(self, name, sp=None):
        self._triggers=[]
        self._name=name
        self._sp=sp
        self._sorted=False

    def reset(self):
        self._triggers=[]
        self._sorted=False

    @property
    def name(self):
        return self._name

    def now(self):
        return datetime.now()

    def dow(self, date):
        return

    def addTrigger(self, trigger: Trigger):
        if trigger is not None:
            self._triggers.append(trigger)
            self._sorted=False
            return trigger

    def on(self, dow: str, t: str, sp=None):
        try:
            return self.addTrigger(Trigger(dow, t, state=True, sp=sp))
        except:
            pass

    def off(self, dow: str, t: str, sp=None):
        try:
            return self.addTrigger(Trigger(dow, t, state=False, sp=sp))
        except:
            pass

    def slot(self, dow: str, t: str, duration: int, sp=None):
        try:
            t0=Trigger(dow, t, state=True, sp=sp)
            t1=Trigger(dow, t0.t(int(duration)), state=False)
            self.addTrigger(t0)
            self.addTrigger(t1)
            return t0, t1
        except:
            pass

    def eval(self, date: datetime = None):
        if not self._sorted:
            self._triggers.sort()
            self._sorted=True

        state=False
        sp=self._sp
        if date is None:
            date=self.now()
        stamp=date.hour*60+date.minute
        if date is not None:
            for t in self._triggers:
                if t.matchDow(date):
                    if stamp>=t.stamp:
                        state=t.state
                        if t.sp is not None:
                            sp=t.sp
                    else:
                        # Triggers are sorted
                        break
        return state, sp


class Schedulers(object):
    def __init__(self):
        self._schedulers={}

    def reset(self):
        for scheduler in self._schedulers.values():
            scheduler.reset()

    def get(self, name):
        try:
            return self._schedulers[name.lower()]
        except:
            pass

    def __getitem__(self, key):
        return self.get(key)

    def __iter__(self):
        return iter(self._schedulers.values())

    def create(self, name, sp=None):
        if name:
            scheduler=self.get(name)
            if not scheduler:
                scheduler=Scheduler(name, sp)
                self._schedulers[name.lower()]=scheduler
            return scheduler

    def eval(self, name, date=None):
        try:
            return self.get(name).eval(date)
        except:
            pass

    def getField(self, row, n, default=None):
        try:
            return row[n].strip()
        except:
            pass
        return default

    def loadcsv(self, f, delimiter=',', dialect='unix', logger=None):
        try:
            # reader=csv.reader(f, delimiter=delimiter, dialect=dialect)
            reader=csv.reader(f, delimiter=delimiter)
            self.reset()
            for row in reader:
                scheduler=self.get(self.getField(row, 0))
                if scheduler:
                    try:
                        trigger=self.getField(row, 1).lower()
                        dow=self.getField(row, 2)
                        if trigger=='on':
                            t=self.getField(row, 3)
                            sp=self.getField(row, 4)
                            scheduler.on(dow, t, sp)
                        elif trigger=='off':
                            t=self.getField(row, 3)
                            sp=self.getField(row, 4)
                            scheduler.off(dow, t, sp)
                        elif trigger=='slot':
                            t=self.getField(row, 3)
                            d=self.getField(row, 4)
                            sp=self.getField(row, 5)
                            scheduler.slot(dow, t, d, sp)
                    except:
                        pass
        except:
            if logger:
                logger.exception('csv')
            pass

    def dump(self):
        t=PrettyTable()
        t.field_names=['Program', 'DOW', 't', 'state', 'sp']
        t.align='l'

        for name in self._schedulers.keys():
            scheduler=self._schedulers[name]
            for trigger in scheduler._triggers:
                t.add_row([name, trigger.dow, trigger.t(), trigger.state, trigger.sp])

        print(t.get_string())


class MBIOTaskScheduler(MBIOTask):
    def initName(self):
        return 'sch'

    @property
    def schedulers(self):
        return self._schedulers

    def onInit(self):
        self._schedulers=Schedulers()
        self._programs={}
        self._timeoutreload=0
        self.config.set('reloadperiod', 0)
        self.config.set('reloadurl', None)

    def onLoadProgram(self, scheduler, xml: XMLConfig):
        if scheduler is not None and xml is not None:
            items=xml.children('*')
            if items:
                for item in items:
                    if item.tag=='on':
                        scheduler.on(item.get('dow'), item.get('time'), item.getFloat('sp'))
                    elif item.tag=='off':
                        scheduler.off(item.get('dow'), item.get('time'), item.getFloat('sp'))
                    elif item.tag=='slot':
                        scheduler.slot(item.get('dow'), item.get('time'), item.get('duration'), item.getFloat('sp'))

    def onLoad(self, xml: XMLConfig):
        items=xml.children('program')
        if items:
            for item in items:
                name=item.get('name')
                if name and not self._schedulers.get(name):
                    sp=item.child('sp')
                    default=None
                    if sp:
                        default=sp.getFloat('default')
                        unit=sp.get('unit', 'C')
                        resolution=item.getFloat('resolution', 0.1)

                    scheduler=self._schedulers.create(name=name, sp=default)
                    program={'state': self.valueDigital('%s_state' % name)}
                    if sp:
                        program['sp']=self.value('%s_sp' % name, unit=unit, resolution=resolution)
                    self._programs[name]=program
                    self.onLoadProgram(scheduler, item.child('triggers'))

        item=xml.child('download')
        if item and item.child('url'):
            try:
                self.valueDigital('comerr', default=False)
                self._timeoutReload=0
                self.config.type=item.get('type', 'csv')
                self.config.reloadperiod=item.getInt('period', 60)
                self.config.reloadurl=item.child('url').text()
                self.logger.error(self.config.url)
                self.reload()
            except:
                pass

    def poweron(self):
        return True

    def poweroff(self):
        return True

    def reload(self):
        self._timeoutReload=self.timeout(60*60)
        if self.config.reloadperiod>0 and self.config.reloadurl:
            try:
                r=requests.get(self.config.reloadurl, timeout=5.0)
                if r and r.ok:
                    data=r.text

                    if self.config.type=='csv':
                        f=io.StringIO(data)
                        self._schedulers.loadcsv(f, logger=self.logger)
                    else:
                        self.logger.warning(data)

                    self.values.comerr.updateValue(False)
                    self._timeoutReload=self.timeout(self.config.reloadperiod*60)
                    return True
            except:
                pass

        self.values.comerr.updateValue(True)
        return False

    def run(self):
        if self.config.reloadperiod>0 and self.isTimeout(self._timeoutReload):
            self.reload()

        for scheduler in self._schedulers:
            state, sp = scheduler.eval()
            try:
                self._programs[scheduler.name]['state'].updateValue(state)
                self._programs[scheduler.name]['sp'].updateValue(sp)
            except:
                pass
        return 1.0


if __name__ == '__main__':
    pass
