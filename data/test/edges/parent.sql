SELECT development.parent.parent AS ":START_ID(Sample)", development.parent.child AS ":END_ID(Sample)", 'Sample' AS ":TYPE", development.parent.deleted AS deleted 
FROM development.parent