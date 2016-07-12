"""Startup script for IPython kernel.

Installs an import hook to configure the matplotlib backend on the fly.

Originally from @minrk at 
https://github.com/minrk/profile_default/blob/master/startup/mplimporthook.py
Repurposed for docker-stacks to address repeat bugs like
https://github.com/jupyter/docker-stacks/issues/235.
"""
import sys
from IPython import get_ipython

class MatplotlibFinder(object):
    """Import hook that notices when matplotlib.pyplot or pylab is imported
    and tries to configure the matplotlib backend appropriately for the
    environment.
    """
    _called = False
    
    def find_module(self, fullname, path=None):
        if self._called:
            # already handled
            return
        
        if fullname not in ('pylab', 'matplotlib.pyplot'):
            # not matplotlib
            return
        
        # don't call me again
        self._called = True
        
        try:
            # remove myself from the import hooks
            sys.meta_path = [loader for loader in sys.meta_path if loader is not self]
        except ValueError:
            pass
        
        ip = get_ipython()
        if ip is None:
            # not in an interactive environment
            return
            
        if ip.pylab_gui_select:
            # backend already selected
            return
            
        if hasattr(ip, 'kernel'):
            # default to inline in kernel environments
            ip.enable_matplotlib('inline')
        else:
            print('enabling matplotlib')
            ip.enable_matplotlib()

# install the finder immediately
sys.meta_path.insert(0, MatplotlibFinder())