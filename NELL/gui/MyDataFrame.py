import pandas

class MyDataFrame(pandas.DataFrame):
    def __finalize__(self, other, method=None, **kwargs):
        return super().__finalize__(other, method, **kwargs)

    def __setitem__(self, key, value):
        super().__setitem__(key, value)
        try: self.change_listener(None)
        except: pass


    @property
    def loc(self):
        loc_idx = super().loc

        class LocIndexer:
            def __getitem__(self, idx):
                return loc_idx.__getitem__(idx)
            
            def __setitem__(self, idx, value):
                loc_idx.__setitem__(idx, value)
                try: self.change_listener(None)
                except: pass          

        result = LocIndexer()
        result.change_listener = self.change_listener
        return result

    def set_change_listener(self, listener):
        self.change_listener = listener