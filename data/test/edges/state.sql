SELECT development.state.child AS ":START_ID(SampleProcess)", development.state.parent AS ":END_ID(SampleProcess)", 'SampleProcess' AS ":TYPE", development.state.deleted AS deleted 
FROM development.state