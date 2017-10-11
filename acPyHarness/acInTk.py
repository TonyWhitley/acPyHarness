from enum import IntEnum
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk

class Status(IntEnum):
  """ Function return status values """
  SUCCESS = 1
  FAIL =    -1

class Control(object):
  master = None
  name = None
  controlId = None
  control = None
  label = None
  image = None
  root = None

controls = []

def acUpdate(deltaT, acUpdateFn):
  """ Handle the way AC calls the update fn at intervals """
  def _tick():
    """ Tk callback function """
    controls[0].root.after(deltaT, _tick)
    acUpdateFn(deltaT)
  
  _tick()     # Set it going
  mainloop()  # Tk main loop handling events




def _scale(x):
  """
  Scale AC co-ord or length to tkinter value
  """
  scaleFactor = 1
  _ret = int(x/scaleFactor)
  return _ret

class acInTk(object):
  """Implement Assetto Corsa app graphics using Tkinter"""
  def __init__(self):
    pass
  def newApp(self, name):
    # VALUE must be a string
    # Creates a new app and returns the corresponding Identifier.
    # returns the App ID on success, -1 otherwise
    _o = Control()
    _o.root = Tk()
    _o.control = Canvas(width=1, height=1, bg='black')

    # pack the canvas into a frame/form
    _o.control.pack(expand=YES, fill=BOTH)
    _o.controlId = len(controls)

    _o.root.protocol("WM_DELETE_WINDOW", self._delete_window)
    controls.append(_o)
    return _o.controlId

  def _delete_window(self):
    """ The main window has been closed, shut down """
    sys.exit(99)

  def setTitle(self, CONTROL_IDENTIFIER,TITLE):
    controls[CONTROL_IDENTIFIER].root.title(TITLE)
    return Status.SUCCESS
    # TITLE must be a string, CONTROL_IDENTIFIER must be a form
    # This function will set the title of the specified App by CONTROL_IDENTIFIER.
    # The function returns 1 on success, -1 otherwise

  def setSize(self, CONTROL_IDENTIFIER,WIDTH,HEIGHT):
      controls[CONTROL_IDENTIFIER].control.config(width = _scale(WIDTH))
      controls[CONTROL_IDENTIFIER].control.config(height = _scale(HEIGHT))
      return Status.SUCCESS
    # WIDTH,HEIGHT must be a floating point numbers
    # This function will set the size of a control specified by CONTROL_IDENTIFIER .
    # The function returns 1 on success, -1 otherwise

  def addLabel(self, CONTROL_IDENTIFIER,VALUE):
    _o = Control()
    label_frame = Frame(controls[CONTROL_IDENTIFIER].control)
    label_frame.pack_propagate(False) # Stops child widgets of label_frame from resizing it

    _o.control = label_frame
    _o.label = Label(label_frame, text=VALUE)
    #_o.control = Label(controls[CONTROL_IDENTIFIER].control, text=VALUE)
    _o.controlId = len(controls)

    controls.append(_o)
    return _o.controlId
    # VALUE must be a string
    # It is possible to add a label to a Window, we need to pass the Window to ac.addLabel and
    # the label name.
    # The function returns 1 on success, -1 otherwise

  def setPosition(self, CONTROL_IDENTIFIER,X,Y):
      controls[CONTROL_IDENTIFIER].control.place(x = _scale(X), y = _scale(Y))
      return Status.SUCCESS
    # X,Y must be a floating point numbers
    # Use ac.setPosition to set the control's position specified by CONTROL_IDENTIFIER in
    # the app.
    # The function returns 1 on success, -1 otherwise

  def setIconPosition(self, CONTROL_IDENTIFIER,X,Y):
    # that removes the background    controls[CONTROL_IDENTIFIER].control.place(relx=X, rely=Y, anchor="c")
    return Status.SUCCESS
    # X,Y must be a floating point numbers, CONTROL_IDENTIFIER must be a form
    # Use ac.setPosition to set the new icon's position instead of the default one.
    # The function returns 1 on success, -1 otherwise

  def setTitlePosition(self, CONTROL_IDENTIFIER,X,Y):
      return Status.SUCCESS
    # X,Y must be a floating point numbers, CONTROL_IDENTIFIER must be a form
    # Use ac.setPosition to set the new title's position inside the app.
    # The function returns 1 on success, -1 otherwise

  def getPosition(self, CONTROL_IDENTIFIER):
      pass
    # CONTROL_IDENTIFIER is the identifier of a control
    # Use ac.getPosition to get the control's position in the parent window, this function returns a
    # python tuple width,height.
    # The function returns the position as a tuple x,y on success, -1 otherwise

  def setText(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be a string, CONTROL_IDENTIFIER is the control that we want to set the
    # text to
    # Set the text of the control specified by CONTROL_IDENTIFIER, with the VALUE text
    # passed as an argument.
    # The function returns 1 on success, -1 otherwise

  def getText(self, CONTROL_IDENTIFIER):
      pass
    # CONTROL_IDENTIFIER is the control that we want to get the text from
    # Use ac.getText to get the control's text.
    # This function returns the coordinates x,y of the control on success, -1 otherwise

  def setBackgroundOpacity(self, CONTROL_IDENTIFIER, VALUE):
    if VALUE == 1:  # tkinter can't do transparent
      controls[CONTROL_IDENTIFIER].control.configure(background='black')
    return Status.SUCCESS
    # VALUE must be a floating point value between 0 and 1
    # Use ac.setBackgroundOpacity to change the alpha channel of the desired control.
    # The function returns 1 on success, -1 otherwise

  def drawBackground(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be 0 or 1
    # Use ac.drawBackground to set the background visible (1)(DEFAULT) or transparent (0)
    # The function returns 1 on success, -1 otherwise

  def drawBorder(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be 0 or 1
    # Use ac.drawBorder to draw the border of the desired control (1) (DEFAULT) or not (0)
    # The function returns 1 on success, -1 otherwise

  def setBackgroundTexture(self, CONTROL_IDENTIFIER, PATH):
    img_name = PATH
    image_pil = Image.open(img_name) #.resize((200, 100), Image.ANTIALIAS)
    imgobj = ImageTk.PhotoImage(image_pil)
    controls[CONTROL_IDENTIFIER].image = imgobj # keep a reference!
    controls[CONTROL_IDENTIFIER].control.create_image(0, 0, image=imgobj, anchor=NW)
    return Status.SUCCESS
    """
      #try:
      im = Image.open(PATH)
      root = controls[CONTROL_IDENTIFIER].master
      controls[CONTROL_IDENTIFIER].image = ImageTk.PhotoImage(im) # keep a reference!
      controls[CONTROL_IDENTIFIER].control.create_image(0, 0, controls[CONTROL_IDENTIFIER].image)
      return Status.SUCCESS
      #except IOError:
      return Status.FAIL
      #except:
      return Status.FAIL
    """
    # PATH starts from Assetto Corsa root folder, CONTROL_IDENTIFIER must be a
    # control identifier
    # Use ac.setBackgroundTexture to draw a specified texture stored in the path specified by
    # PATH as background image for the control specified by CONTROL_IDENTIFIER.
    # The function returns 1 on success, -1 otherwise

  def setFontAlignment(self, CONTROL_IDENTIFIER, ALIGNMENT):
      if ALIGNMENT == 'left':
        _al = 'w'
      if ALIGNMENT == 'right':
        _al = 'e'
      if ALIGNMENT == 'center':
        _al = 'center'
      if controls[CONTROL_IDENTIFIER].label:
        controls[CONTROL_IDENTIFIER].label.configure(anchor = _al)
      else:
        controls[CONTROL_IDENTIFIER].control.configure(anchor = _al)
      return Status.SUCCESS
    # ALIGNMENT is one of the following strings:
    # "left "
    # "right"
    # "center"
    # Use ac.setFontAlignment to set the font alignment of the control text as specified by the
    # ALIGNMENT string.
    # The function returns 1 on success, -1 otherwise

  def setBackgroundColor(self, CONTROL_IDENTIFIER, R,G,B):
      return Status.SUCCESS
    # PATH starts from Assetto Corsa root folder
    # Use ac.setBackgroundColor to set the background color of the window as specified by the
    # R,G,B values
    # The function returns 1 on success, -1 otherwise

  def setVisible(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be 0 or 1
    # It is possible to hide the object using the function ac.setVisible with VALUE set to 1.
    # The function returns 1 on success, -1 otherwise

  def addOnAppActivatedListener(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be a function name defined inside the Python script,
    # CONTROL_IDENTIFIER must be an app.
    # This method set the VALUE function as callback function for the event of app selection on
    # the task bar.
    # The function returns 1 on success, -1 otherwise

  def addOnAppDismissedListener(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be a function name defined inside the Python script,
    # CONTROL_IDENTIFIER must be an app.
    # This method set the VALUE function as callback function for the event of app deselection
    # on the task bar.
    # The function returns 1 on success, -1 otherwise

  def addRenderCallback(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be a function name defined inside the Python script
    # This method set the VALUE function as callback function for the finished rendering event.
    # The function returns 1 on success, -1 otherwise

  def setFontColor(self, CONTROL_IDENTIFIER,R,G,B,A):
      return Status.SUCCESS
    # CONTROL_IDENTIFIER must be a Controlidentifier, R,G,B,A are the color
    # value scaled from 0 to 1
    # This function returns 1 on success, -1 otherwise

  def setFontSize(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # This method set VALUE as new new size of the control's font.
    # The function returns 1 on success, -1 otherwise

  def initFont(self, zero, FONTNAME, ITALIC, BOLD):
      return Status.SUCCESS
    # This method loads the font in memory (stored as font+italic+bold). Should be used at the
    # initialization of the application. The font needs to be saved in the "content/fonts" folder.
    # FONTNAME must be the name of the base font (real name, not filename, so it can be
    # "Arial")
    # ITALIC must be a 0 for non-italic font, 1 for italic font (instance will be "Arial Italic")
    # BOLD must be a 0 for non-bold font, 1 for bold font (instance will be "Arial Bold" or "Arial
    # Italic Bold" is also italic)
    # The function returns 1 on success, -1 otherwise

  def setCustomFont(self, CONTROL_IDENTIFIER, FONTNAME, ITALIC, BOLD):
      return Status.SUCCESS
    # This method create or replace the font of a control. Should not be done without calling
    # "iniFont". The font needs to be saved in the "content/fonts" folder.
    # CONTROL_IDENTIFIER is the control owner of the font
    # FONTNAME must be the name of the base font (real name, not filename, so it can be
    # "Arial")
    # ITALIC must be a 0 for non-italic font, 1 for italic font (instance will be "Arial Italic")
    # BOLD must be a 0 for non-bold font, 1 for bold font (instance will be "Arial Bold" or "Arial
    # Italic Bold" is also italic)
    # The function returns 1 on success, -1 otherwise

  # SPECIFIC CONTROL MANAGEMENT:
  # Button:

  def addButton(self, CONTROL_IDENTIFIER, VALUE):
      pass
    # VALUE must be a string, CONTROL_IDENTIFIER must be a form
    # The function adds a Button to the window specified by CONTROL_IDENTIFIER
    # The function returns the Button ID on success, -1 otherwise

  def addOnClickedListener(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be a function name defined in this file
    # It is possible to associate the button with an event to trigger when it is clicked using this
    # function
    # The function returns 1 on success, -1 otherwise
    # Graph:

  def addGraph(self, CONTROL_IDENTIFIER, VALUE):
      pass
    # VALUE must be a string
    # The function adds a Graph to the window specified in CONTROL_IDENTIFIER
    # The function returns the Graph ID on success, -1 otherwise

  def addSerieToGraph(self, CONTROL_IDENTIFIER, R,G,B):
      return Status.SUCCESS
    # R,G,B must be floating point numbers between 0 and 1
    # To plot some data it is necessary to add a Serie. A serie is a succession of points to plot on
    # the graph.
    # When adding a serie you must specify the color of the serie as argument
    # The function returns 1 on success, -1 otherwise

  def addValueToGraph(self, CONTROL_IDENTIFIER,SERIE_INDEX,VALUE):
      return Status.SUCCESS
    # SERIE_INDEX is the Serie ID in the graph that where VALUE will be added.
    # The function returns 1 on success, -1 otherwise

  def setRange(self, CONTROL_IDENTIFIER,MIN_VALUE,MAX_VALUE,MAX_POINTS):
      return Status.SUCCESS
    # MIN_VALUE,MAX_VALUE,MAX_POINTS must be floating point numbers
    # In order to plot the data inside the Graph it is necessary to specify the amplitude of the
    # ordinates and the maximum number of points to store in memory
    # The function returns 1 on success, -1 otherwise

  # Spinner:

  def addSpinner(self, CONTROL_IDENTIFIER, VALUE):
      pass
    # VALUE must be a string
    # It is possible to add a Spinner using the function
    # The function returns the Spinner ID on success, -1 otherwise

  def setRange(self, CONTROL_IDENTIFIER, MIN_VALUE,MAX_VALUE):
      return Status.SUCCESS
    # MIN_VALUE,MAX_VALUE must be floating point numbers
    # It is possible to set the min and max values of the Control:
    # The function returns 1 on success, -1 otherwise

  def setValue(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be floating point number
    # This function set the "value" parameter of the specific Control if this is an available
    # parameter.
    # This function affects controls like Spinner, Progress Bar or Check Box
    # The function returns 1 on success, -1 otherwise

  def getValue(self, CONTROL_IDENTIFIER):
      pass
    # VALUE must be floating point number
    # This function returns the "value" parameter of the specific Control if this is an available
    # parameter.
    # The function returns the value on success, -1 otherwise

  def setStep(self, CONTROL_IDENTIFIER,VALUE):
      return Status.SUCCESS
    # CONTROL_IDENTIFIER must be a Spinner ID VALUE must be floating point number
    # Set the value added or subtracted when the + or - button is pressed in a Spinner controller.
    # The function returns 1 on success, -1 otherwise

  def addOnValueChangeListener(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be a function name defined inside the Python script
    # It is now possible to associate the spinner with an event to trigger when one of the two
    # buttons is pressed
    # The function returns 1 on success, -1 otherwise

  # Progress Bar :

  def addProgressBar(self, CONTROL_IDENTIFIER, VALUE):
      pass
    # VALUE must be a string
    # It is possible to add a Progress Bar using the function
    # The function returns the Progress Bar ID on success, -1 otherwise

  # Input Text :

  def addInputText(self, CONTROL_IDENTIFIER, VALUE):
      pass
    # VALUE must be a string
    # It is possible to add an Input Text Field using the function
    # The function returns the Input Text ID on success, -1 otherwise

  def setFocus(self, CONTROL_IDENTIFIER, FOCUS):
      return Status.SUCCESS
    # CONTROL_IDENTIFIER must be an Input Text, FOCUS must be 0 or 1
    # If FOCUS is 1, this function sets the Input Text as first responder.
    # The function returns 1 on success, -1 otherwise

  def addOnValidateListener(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be a function name defined inside the Python script
    # It is possible to associate the CONTROL_IDENTIFIER with an event to trigger when the
    # enter key is pressed
    # The function returns 1 on success, -1 otherwise

  # List Box :

  def addListBox(self, CONTROL_IDENTIFIER,NAME):
      pass
    # CONTROL_IDENTIFIER must be a window identifier
    # This method adds a List Box to the window specified by CONTROL_IDENTIFIER
    # The function returns the ListBox ID on success, -1 otherwise

  def addItem(self, CONTROL_IDENTIFIER,NAME):
      pass
    # CONTROL_IDENTIFIER must be a ListBox identifier
    # This method adds a List Box item to the List Box specified.
    # The item's label is specified by the Name string.
    # This function returns the ListBox Item ID on success, -1 otherwise

  def removeItem(self, CONTROL_IDENTIFIER,ID):
      pass
    # CONTROL_IDENTIFIER must be a ListBox identifier
    # This method removes from the List Box the item with ID as identifier
    # This function returns the size of the List Box on success, -1 otherwise

  def getItemCount(self, CONTROL_IDENTIFIER):
      pass
    # CONTROL_IDENTIFIER must be a ListBox identifier
    # This function returns the size of the List Box on success, -1 otherwise

  def setItemNumberPerPage(self, CONTROL_IDENTIFIER,NUMBER):
      return Status.SUCCESS
    # CONTROL_IDENTIFIER must be a ListBox identifier, NUMBER is the number of
    # element to be displayed desired for each page
    # This function sets the number of element displayed for each page in a List Box.
    # This function returns 1 on success, -1 otherwise

  def highlightListBoxItem(self, CONTROL_IDENTIFIER,ID):
      return Status.SUCCESS
    # CONTROL_IDENTIFIER must be a ListBox identifier, ID is the element to be selected
    # This function sets the list box item with ID as identifier as selected.
    # This function returns 1 on success, -1 otherwise

  def addOnListBoxSelectionListener(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be a function name defined inside the Python script
    # Control identifier must be a List Box controller otherwise the function does nothing and
    # returns 0.
    # This method set the VALUE function as callback function for the event of item
    # SELECTION inside a ListBox.
    # The callback function receives as input parameters the Item's NAME and its ID (his position
    # inside the list-box).
    # The function returns 1 on success, -1 otherwise

  def addOnListBoxDeselectionListener(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be a function name defined inside the Python script
    # Control identifier must be a List Box controller otherwise the function does nothing and
    # returns 0.
    # This method set the VALUE function as callback function for the event of item
    # DESELECTION inside a ListBox.
    # The callback function receives as input parameters the Item's NAME and its ID (his position
    # inside the list-box).
    # The function returns 1 on success, -1 otherwise

  def setAllowDeselection(self, CONTROL_IDENTIFIER,ALLOW_DESELECTION):
      return Status.SUCCESS
    # CONTROL_IDENTIFIER must be a ListBox identifier, ALLOW_DESELECTION must
    # be 0 or 1
    # Passing true as a parameter, when the user clicks on a selected item the item is
    # de-selected.
    # In this way there could be 0 or 1 selected item at a given time.
    # If also ac.setAllowMultiSelection is set as true there can be more than 1 selected items at a
    # given time.
    # This function returns 1 on success, -1 otherwise

  def setAllowMultiSelection(self, CONTROL_IDENTIFIER,ALLOW_MULTI_SELECTION):
      return Status.SUCCESS
    # CONTROL_IDENTIFIER must be a ListBox identifier, ALLOW_MULTI_SELECTION
    # must be 0 or 1
    # Passing true as a parameter, when the user clicks on a different item the item is added to
    # the selected item list.
    # In this way there could me more than one selected items at a given time
    # This function returns 1 on success, -1 otherwise

  def getSelectedItems(self, CONTROL_IDENTIFIER):
      pass
    # CONTROL_IDENTIFIER must be a ListBox identifier
    # This method returns the list of the selected items at a given time.
    # This function returns a Python list of Long on success, -1 otherwise

  # Check Box :

  def addCheckBox(self, CONTROL_IDENTIFIER,VALUE):
      pass
    # CONTROL_IDENTIFIER must be a form ,VALUE must be the form's name
    # This function adds a checkbox to the current form passed as CONTROL_IDENTIFIER.
    # The function returns the checkbox created on success, -1 otherwise

  def addOnCheckBoxChanged(self, CONTROL_IDENTIFIER, VALUE):
      return Status.SUCCESS
    # VALUE must be a function name defined inside the Python script
    # Control identifier must be a Check Box controller otherwise the function does nothing and
    # returns 0.
    # This method set the VALUE function as callback function for the event of checkbox
    # SELECTION or DESELECTION inside a ListBox.
    # The callback function receives as input parameters the CheckBox's NAME and its value, 1 if
    # selected, -1 otherwise.
    # The function returns 1 on success, -1 otherwise

  # Text Box :

  def addTextBox(self, CONTROL_IDENTIFIER,NAME):
      return Status.SUCCESS
    # CONTROL_IDENTIFIER form identifier, NAME text box name
    # This method adds a text box (scrollable if the text is longer than the textbox, to the current
    # form.
    # THIS CONTROL IS NOT CURRENTLY WORKING YET, so no set text has been exposed

  # GRAPHICS AND RENDERING :

  def newTexture(self, PATH):
      pass
    # PATH must be a string, the path is considered from AC installation directory.
    # This method loads in memory the texture specified by path and return the size of the stored
    # texture vector.
    # This method returns the texture identifier on success, -1 otherwise.

  def glBegin(self, PRIMITIVE_ID):
      return Status.SUCCESS
    # PRIMITIVE_ID must be an int corresponding to the following ints:
    # 0 : Draw lines
    # 1 : Draw lines Strip
    # 2 : Draw triangles
    # 3 : Draw quads.
    # Begin a rendering of the specified type.
    # This function returns 1 on success, -1 otherwise

  def glEnd(self, void):
      return Status.SUCCESS
    # Finishes the render of a previous specified primitive
    # This function returns 1 on success

  def glVertex2f(self, X,Y):
      return Status.SUCCESS
    # X,Y must be a floating point numbers
    # Adds a 2d point to the rendering queue.
    # This function returns 1 on success, -1 otherwise

  def glColor3f(self, R,G,B):
      return Status.SUCCESS
    # R,G,B rgb coordinates scaled from 0 to 1, must be a floating point numbers
    # set the current rendering color to R,G,B color.
    # This function returns 1 on success, -1 otherwise

  def glColor4f(self, R,G,B,A):
      return Status.SUCCESS
    # R,G,B rgb coordinates scaled from 0 to 1, A alpha component from 0 to 1, all the
    # values must be a floating point numbers
    # set the current rendering color to R,G,B color, with A as transparency.
    # This function returns 1 on success, -1 otherwise

  def glQuad(self, X,Y,WIDTH,HEIGHT):
      return Status.SUCCESS
    # X,Y,WIDTH,HEIGHT must be a floating point numbers
    # draw a quad quickly without using glBegin, ... , glEnd
    # This function returns 1 on success, -1 otherwise

  def glQuadTextured(self, X,Y,WIDTH,HEIGHT,TEXTURE_ID):
      return Status.SUCCESS
    # X,Y,WIDTH,HEIGHT must be a floating point numbers, TEXTURE_ID is the id
    # of the texture previously loaded.
    # draw a quad quickly without using glBegin, ... , glEnd
    # This function returns 1 on success, -1 otherwise
    #





