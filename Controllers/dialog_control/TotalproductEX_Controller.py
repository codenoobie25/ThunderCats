
class TotalproductEXController:
    def __init__(self, view, data):
        self.view = view
        self.data = data

        self.update_ui_counts()

    def update_ui_counts(self):

        fmt = lambda x: f"{x} items"


        if hasattr(self.view, 'gputotalitems'):
                count = self.data.get('GPU', 0)
                self.view.gputotalitems.setText(fmt(count))
            # Update CPU
        if hasattr(self.view, 'cputotal'):
                count = self.data.get('CPU', 0)
                self.view.cputotal.setText(fmt(count))
            # Update Motherboard
        if hasattr(self.view, 'totalmotherboards'):
                count = self.data.get('Motherboard', 0)
                self.view.totalmotherboards.setText(fmt(count))
            # Update Storage
        if hasattr(self.view, 'storagetotal'):
                count = self.data.get('Storage', 0)
                self.view.storagetotal.setText(fmt(count))
            # Update PSU
        if hasattr(self.view, 'psutotal'):
                count = self.data.get('PSU', 0)
                self.view.psutotal.setText(fmt(count))
            # Update RAM
        if hasattr(self.view, 'totalram'):
                count = self.data.get('RAM', 0)
                self.view.totalram.setText(fmt(count))
            # Update Mouse
        if hasattr(self.view, 'totalmouse'):
                count = self.data.get('Mouse', 0)
                self.view.totalmouse.setText(fmt(count))
            # Update Keyboard
        if hasattr(self.view, 'totalkeyboard'):
                count = self.data.get('Keyboard', 0)
                self.view.totalkeyboard.setText(fmt(count))
            # Update Accessory
        if hasattr(self.view, 'totalaccessory'):
                count = self.data.get('Accessory', 0)
                self.view.totalaccessory.setText(fmt(count))