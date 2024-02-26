import os
import streamlit.components.v1 as components
from Diagram import Diagram
# Create a _RELEASE constant. We'll set this to False while we're developing
# the component, and True when we're ready to package and distribute it.
# (This is, of course, optional - there are innumerable ways to manage your
# release process.)
_RELEASE = True

# Declare a Streamlit component. `declare_component` returns a function
# that is used to create instances of the component. We're naming this
# function "_component_func", with an underscore prefix, because we don't want
# to expose it directly to users. Instead, we will create a custom wrapper
# function, below, that will serve as our component's public API.

# It's worth noting that this call to `declare_component` is the
# *only thing* you need to do to create the binding between Streamlit and
# your component frontend. Everything else we do in this file is simply a
# best practice.

if not _RELEASE:
    _component_func = components.declare_component(
        # We give the component a simple, descriptive name ("my_component"
        # does not fit this bill, so please choose something better for your
        # own component :)
        "node_graph",
        # Pass `url` here to tell Streamlit that the component will be served
        # by the local dev server that you run via `npm run start`.
        # (This is useful while your component is in development.)
        url="http://localhost:3001",
    )
else:
    # When we're distributing a production version of the component, we'll
    # replace the `url` param with `path`, and point it to the component's
    # build directory:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/dist")
    print(build_dir)
    _component_func = components.declare_component("node_graph", path=build_dir)

node_types_data = {
    'out': {"color":"rgb(255,0, 192)", "port_selection" : 'out', 'icon': "FaArrowCircleUp"},
    'in': {"color":"rgb(255,0, 192)", "port_selection" : 'in' , 'icon': "FaArrowCircleDown"},
    'both': {"color":"rgb(255,0, 192)", "port_selection" : 'both','icon': "FaCircle" },
}

print(node_types_data)

def node_graph(model, nodesTypes=node_types_data, key=None):
    """Create a new instance of "node_graph".

    Parameters
    ----------
    model: NodeTypesModel
        Model to display on inital render
    key: str or None
        An optional key that uniquely identifies this component. If this is
        None, and the component's arguments are changed, the component will
        be re-mounted in the Streamlit frontend and lose its current state.

    Returns
    -------
    model: NodeTypesModel
        Model to after user made changes
    """
    # Call through to our private component function. Arguments we pass here
    # will be sent to the frontend, where they'll be available in an "args"
    # dictionary.
    #
    # "default" is a special argument that specifies the initial return
    # value of the component before the user has interacted with it.
    component_value = _component_func(model=model, nodesTypes=nodesTypes, key=key, default=0)
    component_value = Diagram(component_value)
    # We could modify the value returned from the component if we wanted.
    # There's no need to do this in our simple example - but it's an option.
    return component_value


if __name__ == '__main__':
    import streamlit as st
    st. set_page_config(layout="wide")
    initialNodes = [
        # {
        #     'id': '1',
        #     'type': 'input',
        #     'data': { 'label': 'input node1' },
        #     'position': { 'x': 250, 'y': 5 },
        # },
        # {
        #     'id': '2',
        #     'type': 'default',
        #     'data': { 'label': 'default node2' },
        #     'position': { 'x': 300, 'y': 5 },
        # },
        ]

    initialEdges = [
        # { 'id': 'e1-2', 'source': '1', 'target': '2' }
        ]

    model = {'nodes': initialNodes, 'edges': initialEdges}
    
    diagram = node_graph(model, key=None)

    st.write(len(str(diagram.diagram)))    
    st.write(diagram.diagram)
    if len(str(diagram))>200:
        node_graph(diagram, key=1)
    st.write('diagram.selected')
    st.write(diagram.selected)
    st.write('diagram.get_all_nodes_node_inputs')
    st.write(diagram.get_all_nodes_node_inputs())
