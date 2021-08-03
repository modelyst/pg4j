SELECT
	parent ":START_ID(SampleProcess)",
	child ":END_ID(SampleProcess)"
FROM
	development.state;
